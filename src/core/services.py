import json

import aioredis
from src.core.settings import redis_url


class RedisService:

    def __init__(self):
        self.redis_conn = aioredis.from_url(redis_url)

    async def add_element_to_set(self, channel, value):
        await self.redis_conn.sadd(channel, value)

    async def remove_element_from_set(self, channel, value):
        await self.redis_conn.srem(channel, value)

    async def get_all_elements_from_set(self, channel):
        return await self.redis_conn.smembers(channel)

    async def pop_one_set_element(self, channel):
        element = await self.redis_conn.spop(channel)
        return element

    async def check_set_element(self, channel, value):
        exist = await self.redis_conn.sismember(channel, value)
        return exist

    async def subscribe_to_channel(self, channel):
        pubsub = self.redis_conn.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

    async def unsubscribe_from_channel(self, pubsub, channel):
        await pubsub.unsubscribe(channel)
        await pubsub.close()

    async def publish_to_channel(self, channel, message):
        await self.redis_conn.publish(channel, json.dumps(message))

    async def close_connection(self):
        await self.redis_conn.close()
