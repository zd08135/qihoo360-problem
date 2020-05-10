
from handlers.BaseHandler import BaseHandler

class RootHandler(BaseHandler):

    def initialize(self, handler):
        super(RootHandler, self).initialize(handler)

    def get(self):
        self.write("Hello, world, Root")


