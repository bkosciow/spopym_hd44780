from machine import Pin
import ubluetooth


class BLE:
    def __init__(self, name, track):
        self.name = name
        self.track = track
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.config(mtu=256)
        self._connected = False
        self.led = Pin(2, Pin.OUT)

        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.led(1)
        self._connected = True

    def disconnected(self):
        self.led(0)
        self._connected = False

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()

        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()

        elif event == 3:
            '''New message received'''
            buffer = self.ble.gatts_read(self.lcd)
            # print(buffer)
            message = buffer.decode('UTF-8').strip()
            # print(message)
            self.track.add_data(message)

    def register(self):
        PLAYER_UUID = '66b2c551-50df-4188-a436-d6858835fbe0'
        BUTTONS_UUID = '66b2c551-50df-4188-a436-d6858835fbe1'
        LCD_UUID = '66b2c551-50df-4188-a436-d6858835fbe2'

        PLAYER = ubluetooth.UUID(PLAYER_UUID)
        BUTTONS = (ubluetooth.UUID(BUTTONS_UUID), ubluetooth.FLAG_NOTIFY)
        LCD = (ubluetooth.UUID(LCD_UUID), ubluetooth.FLAG_WRITE)

        BLE_PLAYER = (PLAYER, (BUTTONS, LCD,))
        SERVICES = (BLE_PLAYER,)
        ((self.buttons, self.lcd),) = self.ble.gatts_register_services(SERVICES)

    def _send(self, data):
        try:
            self.ble.gatts_notify(0, self.buttons, data + '\n')
        except Exception as e:
            print(e)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(
            100,
            bytearray('\x02\x01\x02', 'utf-8') +
            bytearray((len(name) + 1, 0x09)) +
            name
        )

    def send(self, data):
        if self._connected:
            self._send(data)

