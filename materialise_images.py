#!/usr/bin/env python
from aws import bucket, load_data, save_drink
from binascii import a2b_base64


JPEG_DATA_URL_PREFIX = "data:image/jpeg;base64,"
S3_WEB_URL_TEMPLATE = "http://isthebaropen.s3-website-eu-west-1.amazonaws.com/images/{}.jpg"


if __name__ == '__main__':
  drinks, _, _ = load_data(bucket)
  
  for drink_id, drink in drinks.items():
    if drink['image'].startswith(JPEG_DATA_URL_PREFIX):
      data = drink['image'][len(JPEG_DATA_URL_PREFIX):]
      binary_data = a2b_base64(data)
      bucket.put_object(Key="images/{}.jpg".format(drink_id), Body=binary_data, ACL='public-read')
      
      drink['image'] = S3_WEB_URL_TEMPLATE.format(drink_id)
      save_drink(bucket, drinks, drink_id)
      print("Materialised image for {}".format(drink['name']))
