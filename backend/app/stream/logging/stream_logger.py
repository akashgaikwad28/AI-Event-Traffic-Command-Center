from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("websocket_stream")


class StreamLogger:
    @staticmethod
    def client_connected(client_count: int):
        logger.info("client_connected", client_count=client_count)

    @staticmethod
    def client_disconnected(client_count: int):
        logger.info("client_disconnected", client_count=client_count)

    @staticmethod
    def websocket_broadcast_started(topic: str):
        logger.debug("websocket_broadcast_started", topic=topic)

    @staticmethod
    def websocket_broadcast_completed(
        topic: str, payload_size: int, client_count: int, latency_ms: int
    ):
        logger.info(
            "websocket_broadcast_completed",
            topic=topic,
            payload_size=payload_size,
            client_count=client_count,
            latency_ms=latency_ms,
        )

    @staticmethod
    def broadcast_sent(topic: str, payload_size: int, client_count: int):
        logger.info(
            "broadcast_sent",
            topic=topic,
            payload_size=payload_size,
            client_count=client_count,
        )

    @staticmethod
    def message_received(topic: str, payload_size: int):
        logger.info("message_received", topic=topic, payload_size=payload_size)


stream_logger = StreamLogger()
