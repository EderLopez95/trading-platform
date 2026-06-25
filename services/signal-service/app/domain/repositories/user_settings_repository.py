from abc import ABC
from abc import abstractmethod

class UserSettingsRepository(ABC):
    @abstractmethod
    def get_by_user(self, user_id: str):
        pass

    @abstractmethod
    def create_default(self, user_id: str):
        pass

    @abstractmethod
    def update_analysis_status(self, user_id: str, enabled: bool):
        pass
