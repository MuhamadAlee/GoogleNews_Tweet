import pyshorteners

class Url:

    def __init__(self):
        self.url_shortener = pyshorteners.Shortener()

    def make_tiny_urls(self,main_url):
            """
            Make large urls smaller ones
            """
            short_url = self.url_shortener.tinyurl.short(main_url)
            return short_url