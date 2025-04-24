import time
from fastapi import Request, HTTPException
from redis.asyncio import Redis

r = Redis(host="localhost", port=8080, decode_responses=True)

RATE_LIMITS = {
    "authenticated": (10, 60),
    "anonymous": (2, 60), 
}

async def rate_limit(request: Request, username: str | None = None):
    identity = username or request.client.host
    limit_type = "authenticated" if username else "anonymous"
    limit, period = RATE_LIMITS[limit_type]

    now = int(time.time())
    window_start = now - period
    key = f"rate_limit_{identity}"

    await r.zremrangebyscore(key, min=0, max=window_start)
    request_count = await r.zcard(key)
    if request_count >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    await r.zadd(key, {str(now): now})
    await r.expire(key, period)