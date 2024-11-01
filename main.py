from machine import Pin
import time
from machine import I2C
from microplate.charlcd_i2c_driver import CharLcdDriver
from microplate.charlcd_buffered import CharLCD
from microplate.button_worker import ButtonWorker
from display_worker import DisplayWorker
from track_worker import TrackWorker
import esp32
from ble import BLE
from title import Title
from node_config import *
from config import *
import microplate.core as core

display_cfg = {
    'width': 20,
    'height': 4,
    'marker': chr(255),
    'play': "> ",
    'pause': "||",
    'progress_bar': '[                  ]',
    'volume_bar': '________',
    'title_size': 13,
}

i2c = I2C(0, scl=22, sda=21)
devices = i2c.scan()

drv = CharLcdDriver(devices[0])
lcd = CharLCD(20, 4, drv, 0, 0)
lcd.init()

title_display = Title(display_cfg['title_size'])
track_worker = TrackWorker(title_display, 1000)

ble = BLE(NODE_NAME, track_worker)

display_worker = DisplayWorker(lcd, track_worker, title_display, display_cfg, 1000)


core.add_worker(display_worker)
core.add_worker(track_worker)

core.start()
