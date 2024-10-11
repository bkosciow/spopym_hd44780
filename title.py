class Title:
    def __init__(self, size):
        self.title = ""
        self.artist = ""
        self.tick = 1
        self.size = size
        self.pos = 0

    def set_title(self, title):
        self.title = title
        self.pos = 0

    def append_title(self, text):
        self.title = self.title + text
        self.pos = 0

    def set_artist(self, text):
        self.artist = text
        self.pos = 0

    def append_artist(self, text):
        self.artist = self.artist + text
        self.pos = 0

    def get_tick(self):
        title = self.artist + " - " + self.title + "   "
        r = title[self.pos:self.pos + self.size]
        self.pos += 1
        if self.pos > len(title):
            self.pos = 0
        if len(r) < self.size:
            r += title[0:self.size - len(r)]

        return r
