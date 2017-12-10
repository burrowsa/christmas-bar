#!/usr/bin/env python
from flask import Flask, send_file, request, redirect
from flask_socketio import SocketIO, emit, disconnect
import sys
from aws import bucket, load_data, save_drink, save_orders, save_quantities, remove_drink


app = Flask(__name__) 
app.config['SECRET_KEY'] = b"^\x96\xf2\xbeH\xef='T\xf7<\xe8h\xc8\xa8g\x9c\xb1\x86\x84\xf3w\x15W" 
socketio = SocketIO(app, async_mode=None) 
_drinks, _orders, _quantities = load_data(bucket)


@app.before_request
def before_request():
    if not app.debug and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


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

  emit('update', data, broadcast=broadcast)


@socketio.on('place_order', namespace='/v1')
def v1_place_order(message):
  username = message["username"]
  drink_id = message["drinkId"]
  
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


@socketio.on_error('/v1') # handles the '/chat' namespace
def v1_error_handler(e):
  emit('error', "An error occured on {}".format(request.event["message"]))
  print(type(e), file=sys.stderr)
  print(e, file=sys.stderr)


if __name__ == '__main__':
  socketio.run(app, debug=True)
