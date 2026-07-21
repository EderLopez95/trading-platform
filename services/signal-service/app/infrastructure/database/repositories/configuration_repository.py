from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.configuration import Configuration
from app.domain.repositories.configuration_repository import ConfigurationRepository
from app.infrastructure.database.models.configuration import ConfigurationModel
from app.infrastructure.database.mappers.configuration_mapper import ConfigurationMapper

class ConfigurationRepositoryImpl(ConfigurationRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, configuration: Configuration) -> Configuration:
        model = ConfigurationModel(
            id=UUID(configuration.id),
            user_id=UUID(configuration.user_id),
            symbols=configuration.symbols,
            strategies=configuration.strategies,
            params=configuration.params,
            trend_timeframe=configuration.trend_timeframe,
            context_timeframe=configuration.context_timeframe,
            entry_timeframe=configuration.entry_timeframe,
            enabled=configuration.enabled,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return ConfigurationMapper.to_domain(model)

    def get_by_id(self, configuration_id: str) -> Configuration | None:
        model = (
            self.db.query(ConfigurationModel)
            .filter(ConfigurationModel.id == UUID(configuration_id))
            .first()
        )

        if not model:
            return None

        return ConfigurationMapper.to_domain(model)

    def get_by_user(self, user_id: str) -> list[Configuration]:
        models = (
            self.db.query(ConfigurationModel)
            .filter(ConfigurationModel.user_id== UUID(user_id))
            .order_by(ConfigurationModel.created_at.desc())
            .all()
        )

        return [
            ConfigurationMapper.to_domain(model)
            for model in models
        ]

    def get_enabled(self) -> list[Configuration]:
        models = (
            self.db.query(ConfigurationModel)
            .filter(ConfigurationModel.enabled.is_(True))
            .all()
        )

        return [
            ConfigurationMapper.to_domain(model)
            for model in models
        ]
    
    def get_all(self) -> list[Configuration]:
        models = (
            self.db.query(ConfigurationModel)
            .all()
        )

        return [
            ConfigurationMapper.to_domain(model)
            for model in models
        ]

    def update(self, configuration: Configuration) -> Configuration:
        model = (
            self.db.query(ConfigurationModel)
            .filter(ConfigurationModel.id == UUID(configuration.id))
            .first()
        )
        model.symbols = configuration.symbols
        model.strategies = configuration.strategies
        model.params = configuration.params
        model.trend_timeframe = configuration.trend_timeframe
        model.context_timeframe = configuration.context_timeframe
        model.entry_timeframe = configuration.entry_timeframe
        model.enabled = configuration.enabled
        self.db.commit()
        self.db.refresh(model)

        return ConfigurationMapper.to_domain(model)

    def delete(self, configuration_id: str):
        model = (
            self.db.query(ConfigurationModel)
            .filter(ConfigurationModel.id == UUID(configuration_id))
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()

            return True
