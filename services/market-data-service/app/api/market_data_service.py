from app.infrastructure.protos.generated import (
    market_data_pb2,
    market_data_pb2_grpc,
)

from app.application.services.market_data_service import (
    MarketDataService,
)

from app.infrastructure.mt5.mt5_adapter import (
    MT5Adapter,
)

from app.infrastructure.grpc.mappers.candle_mapper import (
    CandleMapper,
)


class MarketDataGrpcService(
    market_data_pb2_grpc.MarketDataServiceServicer
):

    def GetCandles(
        self,
        request,
        context,
    ):
        service = MarketDataService(
            MT5Adapter()
        )

        candles = (
            service.get_candles(
                request.symbol,
                request.timeframe,
                request.count,
            )
        )

        return (
            market_data_pb2.GetCandlesResponse(
                candles=[
                    CandleMapper.to_proto(
                        candle
                    )
                    for candle in candles
                ]
            )
        )