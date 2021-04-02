import json
import logging
import os

logger = logging.getLogger(__name__)


def xdg_dir():
    """Return the XDG_DATA_HOME or default."""
    if os.getenv("XDG_DATA_HOME"):
        return os.getenv("XDG_DATA_HOME")
    return os.path.join(os.getenv("HOME"), ".local", "share")


def data_dir():
    """Return the taskforge state directory."""
    return os.path.join(xdg_dir(), "taskforge")


class _State:
    def __init__(self, loaded_from=None, **kwargs):
        self._loaded_from = loaded_from
        self._data = kwargs

    @classmethod
    def load_file(cls, fn):
        with open(fn) as cfg:
            data = json.load(cfg)
            return cls(loaded_from=fn, **data)

    @classmethod
    def load(cls):
        dirname = data_dir()
        location = os.path.join(dirname, "state.json")
        if os.path.isfile(location):
            return cls.load_file(location)

        if not os.path.isdir(dirname):
            os.makedirs(data_dir(), exist_ok=True)

        return cls(loaded_from=location)

    def save(self):
        if not self._loaded_from:
            logger.error("unexpected state, should have been loaed from a file!")
            return

        with open(self._loaded_from, "w") as cfg_file:
            logger.debug("saving state to: %s", self._loaded_from)
            json.dump(self._data, cfg_file)

    def __getattr__(self, key):
        return self._data.get(key, None)

    def __setattr__(self, key, value):
        if key in ("_data", "_loaded_from"):
            return super().__setattr__(key, value)

        self._data[key] = value


State = _State.load()
