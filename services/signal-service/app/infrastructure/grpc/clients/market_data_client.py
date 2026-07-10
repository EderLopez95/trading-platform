import grpc
from app.config.settings import ENV, MARKET_DATA_SERVICE_HOST, MARKET_DATA_SERVICE_PORT, SIGNAL_SERVICE_SECURE, TRUSTED_CA_CERT
from app.infrastructure.protos.generated import market_data_pb2, market_data_pb2_grpc

class MarketDataClient:
    def __init__(self):
        address = (f"{MARKET_DATA_SERVICE_HOST}:{MARKET_DATA_SERVICE_PORT}")

        if ENV == "prod" and SIGNAL_SERVICE_SECURE:
            with open(TRUSTED_CA_CERT, "rb") as f:
                credentials = grpc.ssl_channel_credentials(f.read())
            self.channel = grpc.secure_channel(address, credentials)
        else:
            self.channel = grpc.insecure_channel(address)

        self.stub = market_data_pb2_grpc.MarketDataServiceStub(self.channel)

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        response = (
            self.stub.GetCandles(
                market_data_pb2.GetCandlesRequest(
                    symbol=symbol,
                    timeframe=timeframe,
                    count=count,
                )
            )
        )

        return response
