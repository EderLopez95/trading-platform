class UserRegistry:
    def __init__(self):
        self._settings = {}

    def load(self, settings):
        self._settings = {
            str(setting.user_id): setting
            for setting in settings
        }

    def update(self, setting):
        self._settings[str(setting.user_id)] = setting

    def is_analysis_enabled(self, user_id: str):
        setting = self._settings.get(str(user_id))

        if not setting:
            return True

        return setting.analysis_enabled

    def count(self):
        
        return len(self._settings)
