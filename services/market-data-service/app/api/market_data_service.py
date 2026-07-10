from app.application.services.market_data_service import MarketDataService
from app.infrastructure.mt5.mt5_container import MT5Container
from app.infrastructure.grpc.mappers.candle_mapper import CandleMapper
from app.infrastructure.protos.generated import market_data_pb2, market_data_pb2_grpc
from app.core.errors.handlers import handle_grpc_exception

class MarketDataGrpcService(market_data_pb2_grpc.MarketDataServiceServicer):
    def GetCandles(self, request, context):
        try:
            service = MarketDataService(MT5Container.get_adapter())
            candles = service.get_candles(
                symbol=request.symbol,
                timeframe=request.timeframe,
                count=request.count,
            )

            return (
                market_data_pb2.GetCandlesResponse(
                    candles=[
                        CandleMapper.to_proto(candle)
                        for candle in candles
                    ]
                )
            )
        
        except Exception as e:
            handle_grpc_exception(context, e)
