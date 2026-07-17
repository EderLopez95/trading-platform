from app.infrastructure.database.repositories.signal_repository import SignalRepositoryImpl

class GetSignalsService:
    def __init__(self, repository: SignalRepositoryImpl):
        self.repository = repository

    def execute(
        self,
        user_id: str,
        symbol: str | None,
        strategy: str | None,
        page: int,
        page_size: int,
    ):
        page = max(page, 1)
        page_size = max(min(page_size, 20), 1)

        return self.repository.search(
            user_id=user_id,
            symbol=symbol,
            strategy=strategy,
            page=page,
            page_size=page_size,
        )
