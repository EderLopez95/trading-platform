from app.infrastructure.mt5.mt5_adapter import MT5Adapter

class MT5Container:
    _instance = None

    @classmethod
    def get_adapter(cls) -> MT5Adapter:
        
        if cls._instance is None:
            cls._instance = MT5Adapter()

        return cls._instance
