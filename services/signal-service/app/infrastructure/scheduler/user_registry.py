class UserRegistry:
    def __init__(self):
        self._users = {}

    def load(self, settings):
        self._users = {
            setting.user_id: setting
            for setting in settings
        }

    def update(self, setting):
        self._users[setting.user_id] = setting

    def user_enabled(self, user_id: str):
        setting = self._users.get(user_id)

        if not setting:
            return True

        return setting.analysis_enabled
