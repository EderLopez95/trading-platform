from abc import ABC, abstractmethod
from app.domain.entities.configuration import Configuration

class ConfigurationRepository(ABC):
    @abstractmethod
    def create(
        self,
        configuration: Configuration,
    ) -> Configuration:
        pass

    @abstractmethod
    def get_by_id(
        self,
        configuration_id: str,
    ) -> Configuration | None:
        pass

    @abstractmethod
    def get_by_user(
        self,
        user_id: str,
    ) -> list[Configuration]:
        pass

    @abstractmethod
    def get_enabled(
        self,
    ) -> list[Configuration]:
        pass

    @abstractmethod
    def update(
        self,
        configuration: Configuration,
    ) -> Configuration:
        pass

    @abstractmethod
    def delete(
        self,
        configuration_id: str,
    ) -> None:
        pass
