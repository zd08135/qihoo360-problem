
from handlers.BaseHandler import BaseHandler

from handlers.FeedTypes import FeedType

class FeedHandler(BaseHandler):

    FETCH_NUM = 10

    def initialize(self, handler):
        BaseHandler.initialize(self, handler)

    def get_feed(self, data):

        uid = data["uid"]
        cursor = data["cursor"]

        timestamp_ms = cursor
        timeline_info = self.handler.feed_model.get_timeline(uid, timestamp_ms, self.FETCH_NUM)
        feed_timelines = []
        for timeline in timeline_info:
            uid = timeline["uid"]
            profile_data = self.handler.user_profile_model.get_profile(uid)
            timeline_data = {"profile": profile_data, "feed": timeline}

            feed_type = timeline["type"]
            if feed_type in [FeedType.CREATE_REPOSITORY, FeedType.CREATE_FORK]:
                repository_id = timeline["data"]["rid"]
                repo_data = self.handler.repository_model.get_repository(repository_id)
                timeline_data["repository"] = repo_data
            elif feed_type in [FeedType.FOLLOW]:
                follow_uid = timeline["data"]["follow_uid"]
                profile_data = self.handler.user_profile_model.get_profile(follow_uid)
                timeline_data["follow"] = profile_data

            feed_timelines.append(timeline_data)

        new_cursor = None
        if timeline_info and len(timeline_info) == self.FETCH_NUM:
            new_cursor = timeline_info[-1]["timestamp"]
        return self.success_responce({
            "timeline": feed_timelines,
            "cursor": new_cursor
        })

    
    def follow(self, data):

        uid = data["uid"]
        follow_uid = data["follow_uid"]
        
        if not self.handler.user_profile_model.is_profile_exists(uid) or not self.handler.user_profile_model.is_profile_exists(follow_uid):
            return self.failure_responce(404, "invalid uids")
        self.handler.feed_model.follow(uid, follow_uid)
        self.handler.feed_model.add_feed(uid, FeedType.FOLLOW, {"follow_uid": follow_uid})

        return self.success_responce({})

    def unfollow(self, data):
        uid = data["uid"]
        follow_uid = data["follow_uid"]
        if not self.handler.user_profile_model.is_profile_exists(uid) or not self.handler.user_profile_model.is_profile_exists(follow_uid):
            return self.failure_responce(404, "invalid uids")
        self.handler.feed_model.unfollow(uid, follow_uid)
        return self.success_responce({})
    
        



        




