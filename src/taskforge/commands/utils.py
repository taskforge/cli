import asyncio
import logging
import sys
from contextlib import contextmanager
from functools import wraps

from yaspin import yaspin
from yaspin.spinners import Spinners

from taskforge.client import Client
from taskforge.client.http import ClientException
from taskforge.config import Config

logger = logging.getLogger(__name__)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except ClientException as exc:
            if exc.status_code == 400:
                print("ERROR!", exc.msg)
            else:
                logger.error(exc.msg)
            sys.exit(exc.status_code)
        except SystemExit as exc:
            sys.exit(exc.code)
        except Exception as exc:
            logger.error("%s", exc)
            sys.exit(1)

    return wrapper


def inject_client(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        client = Client(
            base_url=Config.host,
            token=Config.token,
        )
        kwargs["client"] = client
        try:
            await fn(*args, **kwargs)
        finally:
            await client.close()

    return wrapper


@contextmanager
def spinner(text=""):
    if Config.no_spinners:
        yield None
        return

    with yaspin(Spinners.aesthetic, text=text) as sp:
        yield sp
