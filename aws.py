#!/usr/bin/env python
import json
import boto3


s3 = boto3.resource('s3')
BUCKET_NAME = 'isthebaropen'
bucket = s3.Bucket(BUCKET_NAME)


def put_json(bucket, key, obj):
  bucket.put_object(Key=key, Body=json.dumps(obj))


def load_data(bucket):
  drinks, orders, quantities = {}, {}, {}
  for obj in bucket.objects.all():
    if obj.key.endswith('.json'):
      if obj.key.startswith('drinks/'):
        drink_id = obj.key.split('/', 1)[1].replace('.json', '')
        drinks[drink_id] = json.loads(obj.get()['Body'].read().decode('utf-8'))
        drinks[drink_id]['image'] = drinks[drink_id]['image'].replace('http://isthebaropen.s3-website-eu-west-1.amazonaws.com', 'https://d33d54z991aawx.cloudfront.net')
      elif obj.key.startswith('orders/'):
        user_id = obj.key.split('/', 1)[1].replace('.json', '')
        orders[user_id] = set(json.loads(obj.get()['Body'].read().decode('utf-8')))
      elif obj.key == "quantities.json":
        quantities = json.loads(obj.get()['Body'].read().decode('utf-8'))
      else:
        print("Unknown file: '{}'".format(obj.key))
  return drinks, orders, quantities


def save_drink(bucket, drinks, drink_id):
  put_json(bucket, "drinks/{}.json".format(drink_id), drinks[drink_id])


def remove_drink(bucket, drink_id):
  bucket.delete_objects(Delete=dict(Objects=[dict(Key="drinks/{}.json".format(drink_id))]))
 
  
def save_orders(bucket, orders, user_id):
  put_json(bucket, "orders/{}.json".format(user_id), list(orders[user_id]))
  

def save_quantities(bucket, quantities):
  put_json(bucket, "quantities.json", quantities)
  

def save_data(bucket, orders=None, quantities=None, drinks=None):
  if quantities is not None:
    save_quantities(bucket, quantities)
  
  if orders is not None:
    for user_id in orders:
      save_orders(bucket, orders, user_id)

  if drinks is not None:
    for drink_id in drinks:
      save_drink(bucket, drinks, drink_id)
