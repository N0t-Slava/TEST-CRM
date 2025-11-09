import redis.asyncio as redis
import json


redis = redis.from_url(
    "redis://localhost",
    encoding="utf-8",
    decode_responses=True
)


async def set_cookie(session_id: str, data: dict):
    await redis.set(session_id, json.dumps(data), ex=11)

async def get_cookie(session_id: str):
    data = await redis.get(session_id)
    return json.loads(data) if data else None



