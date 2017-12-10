#!/usr/bin/env python
import pickle
from aws import bucket, save_data


DATA_PATH = '/data/xmasbar.pckl' 


if __name__ == '__main__':
  with open(DATA_PATH, 'rb') as f:
    drinks, orders, quantities = pickle.load(f)
  
  save_data(bucket,
            orders=orders,
            quantities=quantities,
            drinks=drinks)
