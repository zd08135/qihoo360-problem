
from handlers.BaseHandler import BaseHandler

class UserProfileHandler(BaseHandler):

    def initialize(self, handler):
        BaseHandler.initialize(self, handler)
        
    def add_user_data(self, data):
        uid = data["uid"]

        profile_data = {
            "uid": uid,
            "name": data["name"],
            "icon": data["icon"]
        }

        self.handler.user_profile_model.add_profile(uid, profile_data)
        return self.success_responce({})

    def delete_user_data(self, data):
        
        uid = data["uid"]
        self.handler.user_profile_model.delete_profile(uid)
        return self.success_responce({})

    def get_user_data(self, data):
        uid = data["uid"]
        data = self.handler.user_profile_model.get_profile(uid)
        
        return self.success_responce(data)