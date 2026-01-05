import redis
import time

r = redis.Redis(host="redis", port=6379, db=0)

def check_rate_limit(folder_id, limit=10, period=60):
    key = f"folder:{folder_id}:rate"
    current = r.get(key)
    if current and int(current) >= limit:
        return False
    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, period)
    pipe.execute()
    return True
