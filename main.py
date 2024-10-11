from machine import Pin
import time
from machine import I2C
from microplate.charlcd_i2c_driver import CharLcdDriver
from microplate.charlcd_buffered import CharLCD
import esp32
from track import Track
from ble import BLE
from title import Title
from node_config import *
from config import *


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
track = Track(title_display)

ble = BLE(NODE_NAME, track)


def display(display_data):
    # print(display_data)
    time_offset = int(display_data['progress_percent'] * (display_cfg['width']) / 100)
    if time_offset == display_cfg['width']:
        time_offset -= 1

    volume = round(display_data['volume'] * len(display_cfg['volume_bar']) / 100)

    lcd.write('-' + display_data['remaining_minute'] + ':' + display_data['remaining_second'], 0, 0)
    lcd.write(display_cfg['play'] if display_data['playing'] else display_cfg['pause'], 0, 1)
    lcd.write(display_cfg['progress_bar'], 0, 3)
    lcd.write(display_cfg['marker'], time_offset, 3)
    lcd.write(
        display_cfg['marker'] *
        volume +
        display_cfg['volume_bar'][0:len(display_cfg['volume_bar']) - volume], 7, 1)
    lcd.write(title_display.get_tick(), 7, 0)
    lcd.flush()


while True:
    start = time.ticks_ms()

    track.tick()

    display(track.current_data)

    calculated_tick = TICK - time.ticks_diff(time.ticks_ms(), start)
    if calculated_tick < 0.0:
        calculated_tick = 0
    time.sleep_ms(calculated_tick)
