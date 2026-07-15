import uuid
from app.infrastructure.database.models.signal import SignalModel
from app.infrastructure.database.mappers.signal_mapper import SignalMapper

class SignalRepositoryImpl:
    def __init__(self, db):
        self.db = db

    def create(self, signal):
        model = SignalMapper.to_model(signal)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def exists(
        self,
        user_id: str,
        dedup_key: str,
        candle_time,
    ):
        
        return (
            self.db.query(SignalModel)
            .filter(
                SignalModel.user_id == uuid.UUID(user_id),
                SignalModel.dedup_key == dedup_key,
                SignalModel.candle_time == candle_time,
            )
            .first()
            is not None
        )
