import json
import time
from typing import Any

from fastapi import WebSocket

from backend.app.stream.logging.stream_logger import stream_logger


class WebSocketManager:
    """
    Manages WebSocket lifecycle and async broadcasting.
    Abstracted for future Redis Pub/Sub swap.
    """

    def __init__(self):
        # topic -> list of websockets
        self.active_connections: dict[str, list[WebSocket]] = {}
        # Metrics
        self.messages_sent = 0

    async def connect(self, websocket: WebSocket, topic: str = "live_events"):
        await websocket.accept()
        if topic not in self.active_connections:
            self.active_connections[topic] = []
        self.active_connections[topic].append(websocket)
        total = sum(len(conns) for conns in self.active_connections.values())
        stream_logger.client_connected(total)

    def disconnect(self, websocket: WebSocket, topic: str):
        if (
            topic in self.active_connections
            and websocket in self.active_connections[topic]
        ):
            self.active_connections[topic].remove(websocket)
            total = sum(len(conns) for conns in self.active_connections.values())
            stream_logger.client_disconnected(total)

    async def broadcast_to_topic(self, topic: str, message: dict[str, Any]):
        """Async fanout to all clients subscribed to a topic."""
        start_time = time.time()
        stream_logger.websocket_broadcast_started(topic)
        if topic in self.active_connections:
            msg_str = json.dumps(message)
            disconnected = []
            for connection in self.active_connections[topic]:
                try:
                    await connection.send_text(msg_str)
                    self.messages_sent += 1
                except Exception:
                    disconnected.append(connection)

            # Cleanup stale connections
            for stale in disconnected:
                self.disconnect(stale, topic)

            total = len(self.active_connections[topic])
            stream_logger.broadcast_sent(topic, len(msg_str), total)

            latency_ms = int((time.time() - start_time) * 1000)
            stream_logger.websocket_broadcast_completed(
                topic, len(msg_str), total, latency_ms
            )

    def get_metrics(self) -> dict[str, Any]:
        return {
            "active_topics": list(self.active_connections.keys()),
            "total_connections": sum(
                len(conns) for conns in self.active_connections.values()
            ),
            "messages_sent": self.messages_sent,
        }


# Global manager instance
ws_manager = WebSocketManager()
