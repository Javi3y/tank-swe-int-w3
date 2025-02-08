import redis.asyncio as redis
from app.config import settings


class Redis:
    redis_client: redis.Redis | None = None

    @classmethod
    async def connect(
        cls,
        host: str = settings.redis_host,
        port: int = settings.redis_port,
        username=settings.redis_username,
        password=settings.redis_password,
    ):
        try:
            cls.redis_client = redis.Redis(
                host=host, port=port, username=username, password=password
            )
        except redis.RedisError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

        await cls.redis_client

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            await cls.redis_client.aclose()

    @classmethod
    async def insert_string(
        cls, key: str, value: str, expiry_seconds: int | None = None
    ):
        if expiry_seconds:
            await cls.redis_client.setex(key, expiry_seconds, value)
        else:
            await cls.redis_client.set(key, value)

    @classmethod
    async def query_key(cls, key: str):
        value = await cls.redis_client.get(key)
        if value == None:
            return None
        value = value.decode("utf-8")
        return value


async def run_redis():
    await Redis.connect()
    return Redis
