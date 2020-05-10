

import json

from . import BaseUtils

class RepositoryRedis:

    REPOSITORY = "rp:%s"

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def create_repository(self, uid, name):

        repository_id = self.generate_repository_id(uid)
        cur_time_ms = BaseUtils.get_cur_time_ms()
        self.redis_client.hmset(self.REPOSITORY % repository_id, {
            "rid": repository_id,
            "uid": uid,
            "create_time": cur_time_ms,
            "name": name,
            "view": 0,
            "fork": 0,
        })
        return repository_id

    def generate_repository_id(self, uid):
        return "%s.%s" % (uid, BaseUtils.random_string(10))

    def create_fork(self, uid, repository_id):

        repo_data = self.redis_client.hgetall(self.REPOSITORY % repository_id)
        if not repo_data:
            return None
        if uid == repo_data["uid"]:
            return None
        name = repo_data["name"]
        new_rid = self.create_repository(uid, name)
        self.redis_client.hincrby(self.REPOSITORY % repository_id, "fork", 1)

        return new_rid

    def get_repository(self, repository_id):
        return self.redis_client.hgetall(self.REPOSITORY % repository_id)