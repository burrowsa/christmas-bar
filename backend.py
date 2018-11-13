#!/usr/bin/env python
from flask import Flask, send_file, request, redirect
from flask_socketio import SocketIO, emit, disconnect
from flask_ask import Ask, statement, session as ask_session, delegate, request as ask_request
import sys, json
from aws import bucket, load_data, save_drink, save_orders, save_quantities, remove_drink
from binascii import a2b_base64
import random


app = Flask(__name__) 
app.config['SECRET_KEY'] = b"^\x96\xf2\xbeH\xef='T\xf7<\xe8h\xc8\xa8g\x9c\xb1\x86\x84\xf3w\x15W" 
ask = Ask(app, '/alexa')
app.config['ASK_VERIFY_REQUESTS'] = False
socketio = SocketIO(app, async_mode=None) 


_drinks, _orders, _quantities = load_data(bucket)


JPEG_DATA_URL_PREFIX = "data:image/jpeg;base64,"
S3_WEB_URL_TEMPLATE = "http://isthebaropen.s3-website-eu-west-1.amazonaws.com/images/{}.jpg"


@app.route('/')
def index():
  return send_file('index.html')


def emit_data(orders=False, quantities=False, drinks=False, broadcast=False):
  data = dict()
  if orders:
    data['orders'] = { k: list(v) for k, v in _orders.items() }
  if quantities:
    data['quantities'] = _quantities 
  if drinks:
    data['drinks'] = _drinks
  
  if hasattr(request, 'namespace'): 
    emit('update', data, broadcast=broadcast)
  else:
    socketio.emit('update', data, broadcast=broadcast, namespace='/v1')


@socketio.on('place_order', namespace='/v1')
def v1_place_order(message):
  username = message["username"]
  drink_id = message["drinkId"]
  _place_order_impl(username, drink_id)


def _place_order_impl(username, drink_id):
  user_orders = _orders.setdefault(username, set())
  quantity_remaining = _quantities.get(drink_id, 0)
  if drink_id not in user_orders and quantity_remaining > 0:
    user_orders.add(drink_id)
    _quantities[drink_id] = quantity_remaining - 1

    save_orders(bucket, _orders, username)
    save_quantities(bucket, _quantities)
    emit_data(orders=True, quantities=True, broadcast=True)


@socketio.on('cancel_order', namespace='/v1')
def v1_cancel_order(message):
  username = message["username"]
  drink_id = message["drinkId"]
  
  user_orders = _orders.setdefault(username, set())
  if drink_id in user_orders:
    user_orders.remove(drink_id)
    _quantities[drink_id] = _quantities.get(drink_id, 0) + 1
  
  save_orders(bucket, _orders, username)
  save_quantities(bucket, _quantities)
  emit_data(orders=True, quantities=True, broadcast=True)


@socketio.on('fulfil_order', namespace='/v1')
def v1_fulfil_order(message):
  username = message["username"]
  drink_id = message["drinkId"]
  
  user_orders = _orders.setdefault(username, set())
  if drink_id in user_orders:
    user_orders.remove(drink_id)
  
  save_orders(bucket, _orders, username)
  emit_data(orders=True, broadcast=True)


@socketio.on('adjust_quantity', namespace='/v1')
def v1_adjust_quantity(message):
  drink_id = message["drinkId"]
  delta = int(message["delta"])
  
  _quantities[drink_id] = _quantities.get(drink_id, 0) + delta
  
  save_quantities(bucket, _quantities)
  emit_data(quantities=True, broadcast=True)


@socketio.on('reload_drink', namespace='/v1')
def v1_reload_drink(message):
  drink_id = message["drinkId"]
  if drink_id in _drinks:
    emit('update_drink', {drink_id: _drinks[drink_id]})
  else:
    emit('remove_drink', dict(drinkId=drink_id))


@socketio.on('save_drink', namespace='/v1')
def v1_save_drink(message):
  assert len(message.keys()) == 1
  
  drink_id = list(message.keys())[0]
  _drinks[drink_id] = message[drink_id]
  drink = _drinks[drink_id] 
  
  if 'image' in drink and drink['image'].startswith(JPEG_DATA_URL_PREFIX):
    data = drink['image'][len(JPEG_DATA_URL_PREFIX):]
    binary_data = a2b_base64(data)
    bucket.put_object(Key="images/{}.jpg".format(drink_id), Body=binary_data, ACL='public-read')

    drink['image'] = S3_WEB_URL_TEMPLATE.format(drink_id)
  
  save_drink(bucket, _drinks, drink_id)
  emit('update_drink', {drink_id: _drinks[drink_id]}, broadcast=True)


@socketio.on('delete_drink', namespace='/v1')
def v1_delete_drink(message):
  drink_id = message["drinkId"]
  
  if drink_id in _drinks:
    remove_drink(bucket, drink_id)
    del _drinks[drink_id]
    emit('remove_drink', dict(drinkId=drink_id), broadcast=True)


@socketio.on('connect', namespace='/v1')
def v1_connect():
  emit_data(orders=True, quantities=True, drinks=True)


@socketio.on_error('/v1')
def v1_error_handler(e):
  emit('error', "An error occured on {}".format(request.event["message"]))
  print(type(e), file=sys.stderr)
  print(e, file=sys.stderr)
  

def resolve_synonym(name, value):
  try:
    return ask_request['intent']['slots'][name]['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
  except KeyError:
    return value


def find_drink(drink):
  for d_id, d in _drinks.items():
    if d["name"].lower().strip() == drink.lower().strip():
      return d_id
  return None
  

def find_person(person):
  for u in _orders:
    if u.lower().strip() == person.lower().strip():
      return u
  return None


@ask.intent('OrderDrink')
def alexa_order_drink(person, drink):
  if ask_session['dialogState'] != 'COMPLETED' or drink is None or person is None:
    return delegate(speech=None)  # speech should not be needed

  person = resolve_synonym('person', person)  
  username = find_person(person)
  if username is None:
    return statement("Sorry I don't know {}".format(person))

  drink = resolve_synonym('drink', drink)
  drink_id = find_drink(drink)
  if drink_id is None:
    return statement("Sorry, I could not find a drink called {}".format(drink))

  quantity_remaining = _quantities.get(drink_id, 0)

  if quantity_remaining < 1:
    return statement("Sorry, but we have run out of {}".format(drink))

  _place_order_impl(username, drink_id)
    
  return statement(random.choice([
                                 "I've notified the butler",
                                 "Okay",
                                 "Your drink is on its way",
                                 "I'll let him know",
                                 ]))


if __name__ == '__main__':
  socketio.run(app, debug=True)
