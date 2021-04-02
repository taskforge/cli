import asyncio
from functools import wraps

from taskforge.client import Client


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def inject_client(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        client = Client()
        kwargs["client"] = client
        try:
            await fn(*args, **kwargs)
        finally:
            await client.close()
    return wrapper