import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from app.config.settings import JWT_SECRET, JWT_ALGORITHM
from app.infrastructure.grpc.clients.providers import get_signal_client

logger = logging.getLogger("gateway")
router = APIRouter()
WS_POLICY_VIOLATION = 1008

def _authenticate(token: str | None) -> str | None:
    if not token:

        return None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        
        return None

    return payload.get("sub")

def _to_payload(signal) -> dict:

    return {
        "id": signal.id,
        "symbol": signal.symbol,
        "strategy": signal.strategy,
        "signal": signal.signal,
        "trend_timeframe": signal.trend_timeframe,
        "context_timeframe": signal.context_timeframe,
        "entry_timeframe": signal.entry_timeframe,
        "price": signal.price,
        "signal_time": signal.signal_time,
    }

@router.websocket("/signals")
async def stream_signals(websocket: WebSocket):
    user_id = _authenticate(websocket.query_params.get("token"))

    if not user_id:
        await websocket.close(code=WS_POLICY_VIOLATION)

        return

    await websocket.accept()

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue = asyncio.Queue()
    stream = get_signal_client().stream_signals(user_id)

    def consume():
        try:
            for signal in stream:
                loop.call_soon_threadsafe(queue.put_nowait, signal)
        except Exception:
            pass
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    consumer = loop.run_in_executor(None, consume)

    async def watch_disconnect():
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            return

    disconnect_task = asyncio.create_task(watch_disconnect())

    try:
        while True:
            producer = asyncio.ensure_future(queue.get())
            done, _ = await asyncio.wait(
                {producer, disconnect_task},
                return_when=asyncio.FIRST_COMPLETED,
            )

            if disconnect_task in done:
                producer.cancel()
                break

            signal = producer.result()

            if signal is None:
                break

            await websocket.send_json(_to_payload(signal))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("signal_ws_error", extra={"error": str(e)})
    finally:
        stream.cancel()
        disconnect_task.cancel()
        consumer.cancel()

        try:
            await websocket.close()
        except RuntimeError:
            pass
