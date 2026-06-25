import asyncio
from datetime import datetime, timezone
from app.infrastructure.scheduler.registry_container import configuration_registry, user_registry

class SignalEngine:
    async def run(self):
        while True:
            now = datetime.now(timezone.utc)

            for configuration in (configuration_registry.get_all()):
                if not (user_registry.user_enabled(configuration.user_id)):
                    continue

                print(
                    f"[{now}] checking {configuration.id}"
                )

            await asyncio.sleep(1)
