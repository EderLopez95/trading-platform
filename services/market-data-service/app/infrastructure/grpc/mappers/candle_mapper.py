from app.infrastructure.protos.generated import market_data_pb2

class CandleMapper:
    @staticmethod
    def to_proto(candle):
        return (
            market_data_pb2.CandleDto(
                timestamp=int(candle.timestamp.timestamp()),
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
            )
        )
