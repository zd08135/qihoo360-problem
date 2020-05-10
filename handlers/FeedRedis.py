

import json

from . import BaseUtils

class FeedRedis:

    FOLLOWS = "fw:%s"
    FANS = "fn:%s"

    FEEDS_CONTENTS = "fc:%s"
    FEED_SEQUENCE = "fs:%s"
    USER_TIMELINE = "ut:%s"

    TIMELINE_EXPIRE_TIME = 1000 * 86400 * 3 # 3 days

    # design: 
    # when A create a feed, it will generate a new feed_id and send to fans
    # each fan add the feed_id into own timeline
    # if B subscribe A. Get the feed_ids from last 3 days, and remove in B's timeline
    # When user query's timeline, query each data and return, the cursor is the timestamp of last resp

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def follow(self, uid, follow_uid):

        follow_key = self.FOLLOWS % uid
        fan_key = self.FOLLOWS % follow_uid

        self.redis_client.sadd(follow_key, follow_uid)
        self.redis_client.sadd(fan_key, uid)
    
    def unfollow(self, uid, follow_uid):

        follow_key = self.FOLLOWS % uid
        fan_key = self.FOLLOWS % follow_uid

        self.redis_client.srem(follow_key, follow_uid)
        self.redis_client.srem(fan_key, uid)
        
        self.remove_feed(uid, follow_uid)

    def add_feed(self, uid, feed_type, feed_data):
        cur_time = BaseUtils.get_cur_time_ms()
        feed_id = self.generate_feed_id(uid, cur_time)

        feed_content_key = self.FEEDS_CONTENTS % feed_id
        self.redis_client.hmset(feed_content_key, {"type": feed_type, "uid": uid, "data": json.dumps(feed_data)})
        
        feed_sequence_key = self.FEED_SEQUENCE % uid
        self.redis_client.zadd(feed_sequence_key, {feed_id: cur_time})

        # add feed_id to my fans
        fan_key = self.FOLLOWS % uid
        fan_uids = self.redis_client.smembers(fan_key)
        for fan_uid in fan_uids:
            self.redis_client.zadd(self.USER_TIMELINE % fan_uid, {feed_id: cur_time})
    
    def remove_feed(self, uid, follow_uid):
        cur_time = BaseUtils.get_cur_time_ms()
        feed_sequence_key = self.FEED_SEQUENCE % follow_uid
        feed_ids = self.redis_client.zrangebyscore(feed_sequence_key, cur_time - self.TIMELINE_EXPIRE_TIME, cur_time)
        for feed_id in feed_ids:
            self.redis_client.zrem(self.USER_TIMELINE % uid, feed_id)

    
    def generate_feed_id(self, uid, timestamp_ms):
        return "%s.%s" % (uid, BaseUtils.random_string(16))

    def get_timeline(self, uid, timestamp_ms, num):

        if timestamp_ms is None:
            timestamp_ms = BaseUtils.get_cur_time_ms()

        feed_id_timelines = self.redis_client.zrangebyscore(self.USER_TIMELINE % uid, "-inf", timestamp_ms-1, 0, num, withscores=True)
        feed_timelines = []
        for feed_info in feed_id_timelines:
            feed_id = feed_info[0]
            timestamp_ms = feed_info[1]
            feed_content_key = self.FEEDS_CONTENTS % feed_id
            feed_content = self.redis_client.hgetall(feed_content_key)
            feed_timelines.append({
                "feed_id": feed_id,
                "timestamp": timestamp_ms,
                "type": feed_content["type"],
                "uid": feed_content["uid"],
                "data": json.loads(feed_content["data"]),
            })

        return feed_timelines

