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


def inject_client(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        client = Client(
            base_url=Config.host,
            token=Config.token,
        )
        kwargs["client"] = client
        try:
            fn(*args, **kwargs)
        except ClientException as exc:
            if exc.status_code == 400:
                logger.error(exc.msg)
            else:
                logger.exception(exc)
            sys.exit(exc.status_code)
        except Exception as exc:
            logger.exception(exc)
            sys.exit(1)
        finally:
            client.close()

    return wrapper


@contextmanager
def spinner(text="", disabled=False):
    if Config.no_spinners or disabled:
        yield None
    else:
        with yaspin(Spinners.aesthetic, text=text) as sp:
            yield sp
