from fastapi import APIRouter, Depends, Query
from app.api.dependencies.auth import get_current_user
from app.infrastructure.grpc.clients.signal_client import SignalClient
from app.application.services.signal_service import SignalService
from app.api.schemas.signal import (
    SignalResponse,
    SignalsResponse,
    StrategyResponse,
    StrategiesResponse,
    SymbolResponse,
    SymbolsResponse,
    TimeframeResponse,
    TimeframesResponse,
)

router = APIRouter()

def get_service():

    return SignalService(SignalClient())

@router.get("/signals")
def get_signals(
    symbol: str | None = Query(default=None),
    strategy: str | None = Query(default=None),
    page: int = Query(default=1),
    page_size: int = Query(default=20),
    current_user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    response = (
        service.get_signals(
            user_id=current_user.user_id,
            symbol=symbol,
            strategy=strategy,
            page=page,
            page_size=page_size,
        )
    )

    return SignalsResponse(
        signals=[
            SignalResponse(
                id=signal.id,
                symbol=signal.symbol,
                strategy=signal.strategy,
                signal=signal.signal,
                trend_timeframe=signal.trend_timeframe,
                context_timeframe=signal.context_timeframe,
                entry_timeframe=signal.entry_timeframe,
                price=signal.price,
                signal_time=signal.signal_time,
            )
            for signal in response.signals
        ],
        page=response.page,
        page_size=response.page_size,
        total=response.total,
    )

@router.get("/strategies")
def get_strategies(
    service: SignalService = Depends(get_service),
):
    response = service.get_strategies()

    return StrategiesResponse(
        strategies=[
            StrategyResponse(
                id=strategy.id,
                name=strategy.name,
            )
            for strategy in response.strategies
        ]
    )

@router.get("/symbols")
def get_symbols(
    search: str | None = Query(default=None),
    service: SignalService = Depends(get_service),
):
    response = service.get_symbols(search=search)

    return SymbolsResponse(
        symbols=[
            SymbolResponse(
                symbol=symbol.symbol,
            )
            for symbol in response.symbols
        ]
    )

@router.get("/timeframes")
def get_timeframes(
    service: SignalService = Depends(get_service),
):
    
    response = service.get_timeframes()

    return TimeframesResponse(
        timeframes=[
            TimeframeResponse(
                timeframe=timeframe.timeframe,
            )
            for timeframe in response.timeframes
        ]
    )
