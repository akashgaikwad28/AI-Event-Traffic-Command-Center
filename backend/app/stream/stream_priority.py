import asyncio

from backend.app.stream.dto.stream_models import StreamEvent


class EventPriorityQueue:
    """
    Ensures CRITICAL alerts are processed first and prevents websocket flooding.
    """

    def __init__(self):
        self.queue = asyncio.PriorityQueue()

    async def enqueue(self, event: StreamEvent):
        # PriorityQueue sorts lowest first, so we invert the priority level
        priority_score = -event.priority_level
        await self.queue.put((priority_score, event))

    async def dequeue(self) -> StreamEvent:
        _, event = await self.queue.get()
        return event

    def is_empty(self) -> bool:
        return self.queue.empty()
