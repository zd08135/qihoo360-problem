
from handlers.BaseHandler import BaseHandler
from handlers.FeedTypes import FeedType

class RepositoryHandler(BaseHandler):

    def initialize(self, handler):
        BaseHandler.initialize(self, handler)

    def create_repository(self, data):

        uid = data["uid"]
        name = data["name"]

        rid = self.handler.repository_model.create_repository(uid, name)
        self.handler.feed_model.add_feed(uid, FeedType.CREATE_REPOSITORY, {"rid": rid})
        return self.success_responce({'rid': rid})

    def create_fork(self, data):

        uid = data["uid"]
        repository_id = data["rid"]

        new_rid = self.handler.repository_model.create_fork(uid, repository_id)
        if not new_rid:
            return self.failure_responce(400, "fork failed")
        self.handler.feed_model.add_feed(uid, FeedType.CREATE_FORK, {"rid": new_rid})
        return self.success_responce({'rid': new_rid})