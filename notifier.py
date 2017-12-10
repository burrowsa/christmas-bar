#!/usr/bin/env python
from socketIO_client import SocketIO, BaseNamespace
import RPi.GPIO as GPIO


BUTLER_PIN=3


class V1(BaseNamespace):
  def on_update(self, msg):
    if "orders" in msg and msg["orders"]:
      butler=False
      for v in msg["orders"].values():
        if len(v):
          butler=True
    
      GPIO.output(BUTLER_PIN, butler)


if __name__ == "__main__":
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(BUTLER_PIN, GPIO.OUT)
  socketIO = SocketIO('https://isthebaropen.co.uk', verify=False)
  socketIO.define(V1, '/v1')
  socketIO.wait()

