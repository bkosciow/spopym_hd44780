from microplate.module import ModuleInterface


class DisplayWorker(ModuleInterface):
    def __init__(self, lcd, track_worker, title_display, display_cfg, tick):
        super().__init__(None, tick)
        self.display_cfg = display_cfg
        self.lcd = lcd
        self.track_worker = track_worker
        self.title_display = title_display

    def action(self):
        if self.track_worker.current_data is None:
            return
        if not self.track_worker.ble:
            self.track_worker.reset()

        # print(display_data)
        time_offset = int(self.track_worker.current_data['progress_percent'] * (self.display_cfg['width']) / 100)
        if time_offset == self.display_cfg['width']:
            time_offset -= 1

        volume = round(self.track_worker.current_data['volume'] * len(self.display_cfg['volume_bar']) / 100)

        self.lcd.write('-' + self.track_worker.current_data['remaining_minute'] + ':' + self.track_worker.current_data['remaining_second'], 0, 0)
        self.lcd.write(self.display_cfg['play'] if self.track_worker.current_data['playing'] else self.display_cfg['pause'], 0, 1)
        self.lcd.write(self.display_cfg['ble_on'] if self.track_worker.ble else self.display_cfg['ble_off'], 5, 1)
        self.lcd.write(self.display_cfg['progress_bar'], 0, 3)
        self.lcd.write(self.display_cfg['marker'], time_offset, 3)
        self.lcd.write(
            self.display_cfg['marker'] *
            volume +
            self.display_cfg['volume_bar'][0:len(self.display_cfg['volume_bar']) - volume], 7, 1)
        self.lcd.write(self.title_display.get_tick(), 7, 0)
        self.lcd.flush()