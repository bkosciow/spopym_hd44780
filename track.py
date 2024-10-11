


class Track:
    def __init__(self, title):
        self.i2k = [
            'title',
            'artist',
            'length',
            'progress',
            'volume',
            'playing',
            'repeat',
            'shuffle',
        ]
        self.title = title
        self.current_data = self.empty_data()

    def time_to_display(self, data, filler="0"):
        if data < 0:
            data = filler * 2
        elif data < 10:
            data = filler + str(data)
        elif data > 99:
            data = "99"
        else:
            data = str(data)

        return data

    def empty_data(self):
        result = {
            'title': "",
            'artist': '',
            'total_minute': "00",
            'total_second': "00",
            'current_minute': "00",
            'current_second': "00",
            'remaining_minute': "00",
            'remaining_second': "00",
            'progress_percent': 0,
            'time_offset': 0,
            'volume': 0,
            'playing': False,
            'repeat': False,
            'shuffle': False,
            'total': 0,
            'progress': 0,
        }
        self.title.set_title("")
        self.title.set_artist("")
        # self.title_display.set(result['title'])

        return result

    def parse_title(self, text, order):
        if order == '0':
            self.title.set_title(text)
        else:
            self.title.append_title(text)

        print(text)

    def parse_artist(self, text, order):
        if order == '0':
            self.title.set_artist(text)
        else:
            self.title.append_artist(text)
        print(text)

    def parse_length(self, text):
        total = round(float(text))
        self.current_data['total'] = total
        self.current_data['total_minute'] = self.time_to_display(int(self.current_data['total'] // 60))
        self.current_data['total_second'] = self.time_to_display(int(self.current_data['total'] % 60))

    def parse_progress(self, text):
        progress = round(float(text))
        self.current_data['progress'] = progress

    def parse_volume(self, text):
        self.current_data['volume'] = int(text)

    def parse_playing(self, text):
        self.current_data['playing'] = text == "True"

    def parse_repeat(self, text):
        self.current_data['repeat'] = text != "off"

    def parse_shuffle(self, text):
        self.current_data['shuffle'] = text == "True"

    def tick(self):
        if not self.current_data['playing']:
            return

        self.current_data['progress'] += 1
        if self.current_data['progress'] > self.current_data['total']:
            self.current_data['progress'] = self.current_data['total']

        self.current_data['remaining_minute'] = self.time_to_display(
            int(self.current_data['total'] - self.current_data['progress']) // 60)
        self.current_data['remaining_second'] = self.time_to_display(
            int(self.current_data['total'] - self.current_data['progress']) % 60)
        self.current_data['progress_percent'] = int(self.current_data['progress'] * 100 / self.current_data['total'])

    def add_data(self, message):
        type = message[0]
        order = message[1]
        text = message[2:]
        # print(type, order, text)
        if type == '0':
            self.parse_title(text, order)
        if type == '1':
            self.parse_artist(text, order)
        if type == '2':
            self.parse_length(text)
        if type == '3':
            self.parse_progress(text)
        if type == '4':
            self.parse_volume(text)
        if type == '5':
            self.parse_playing(text)
        if type == '6':
            self.parse_repeat(text)
        if type == '7':
            self.parse_shuffle(text)
