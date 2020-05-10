
class UserProfileRedis:

    USER_PROFILE_KEY = "upk:%s"

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def add_profile(self, uid, profile_data):
        key = self.USER_PROFILE_KEY % uid
        self.redis_client.hmset(key, profile_data)
    
    def delete_profile(self, uid):
        self.redis_client.delete(self.USER_PROFILE_KEY % uid)
    
    def is_profile_exists(self, uid):
        return self.redis_client.exists(self.USER_PROFILE_KEY % uid)
    
    def get_profile(self, uid):
        key = self.USER_PROFILE_KEY % uid
        return self.redis_client.hgetall(key)
    