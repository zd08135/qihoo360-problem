
import tornado
import redis

from handlers.RootHandler import RootHandler
from handlers.FeedHandler import FeedHandler
from handlers.FeedRedis import FeedRedis
from handlers.UserProfileHandler import UserProfileHandler
from handlers.UserProfileRedis import UserProfileRedis
from handlers.RepositoryHandler import RepositoryHandler
from handlers.RepositoryRedis import RepositoryRedis

class WebService:

    def __init__(self):
        self.application = None

    def init(self):
        self.setup_handlers()
        self.redis_client = redis.Redis("127.0.0.1", 6379, charset="utf-8", decode_responses=True)
        
        self.user_profile_model = UserProfileRedis(self.redis_client)
        self.feed_model = FeedRedis(self.redis_client)
        self.repository_model = RepositoryRedis(self.redis_client)

    def setup_handlers(self):
        handlers = [
            (r"/", RootHandler, dict(handler=self)),
            (r"/api/feed/(.*)", FeedHandler, dict(handler=self)),
            (r"/api/repository/(.*)", RepositoryHandler, dict(handler=self)),
            (r"/api/profile/(.*)", UserProfileHandler, dict(handler=self)),
        ]

        self.application = tornado.web.Application(handlers)

    def start(self):
        self.application.listen(8888)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    web_service = WebService()
    web_service.init()
    web_service.start()
