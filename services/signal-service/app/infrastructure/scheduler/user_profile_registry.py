class UserProfileRegistry:
    def __init__(self):
        self._profiles = {}

    def load(self, profiles):
        self._profiles = {
            profile.user_id: profile
            for profile in profiles
        }

    def update(self, profile):
        self._profiles[
            profile.user_id
        ] = profile

    def get(self, user_id: str):
        
        return self._profiles.get(user_id)

    def count(self):
        
        return len(self._profiles)
