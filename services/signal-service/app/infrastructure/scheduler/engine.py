import asyncio
from datetime import datetime, timezone
from .utils import should_execute

class SignalEngine:
    def __init__(self, registry):
        self.registry = registry

    async def run(self):
        while True:
            now = datetime.now(timezone.utc)
            for config in self.registry.all():                
                if not config.enabled:
                    continue
                if should_execute(
                    config,
                    now,
                ):
                    print(
                        "EXECUTING",
                        config.id,
                    )

            await asyncio.sleep(1)
