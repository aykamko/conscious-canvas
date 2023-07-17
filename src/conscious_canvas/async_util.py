import asyncio

class YieldingQueue(asyncio.Queue):
    """
    A queue that yields to the event loop after every put.
    """
    async def put(self, item):
        result = await super().put(item)
        await asyncio.sleep(0)
        return result