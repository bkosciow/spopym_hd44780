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

power_led = Pin(16, Pin.OUT)

display_cfg = {
    'width': 20,
    'height': 4,
    'marker': chr(255),
    'play': "> ",
    'pause': "||",
    'progress_bar': '[                  ]',
    'volume_bar': '________',
    'title_size': 13,
    'ble_on': 'B',
    'ble_off': '-',
    'shuffle_on': 'S',
    'shuffle_off': ' ',
    'repeat_on': 'R',
    'repeat_off': ' ',
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


def click_callback(pin):
    print("pin : ", pin)


def previous_callback(pin):
    ble.send('prev')


def play_callback(pin):
    ble.send('play')


def stop_callback(pin):
    ble.send('stop')


def next_callback(pin):
    ble.send('next')


btns = ButtonWorker()
btns.add_button(23, 200, previous_callback)
btns.add_button(19, 200, stop_callback)
btns.add_button(18, 200, play_callback)
btns.add_button(5, 200, next_callback)
btns.add_button(17, 200, click_callback)

core.add_worker(btns)
core.add_worker(display_worker)
core.add_worker(track_worker)

power_led.on()
core.start()

