from app.domain.models.models import ConfigurationModel
from app.infrastructure.database.mappers.configuration_mapper import ConfigurationMapper

def get_enabled(self):

    rows = (
        self.db.query(
            ConfigurationModel
        )
        .filter(
            ConfigurationModel.enabled.is_(True)
        )
        .all()
    )

    return [
        ConfigurationMapper.to_domain(row)
        for row in rows
    ]
