import os

import yaml


def xdg_dir():
    """Return the XDG_CONFIG_HOME or default."""
    if os.getenv("XDG_CONFIG_HOME"):
        return os.getenv("XDG_CONFIG_HOME")
    return os.path.join(os.getenv("HOME"), ".config")


def config_dir():
    """Return the taskforge configuration directory."""
    return os.path.join(xdg_dir(), "taskforge")


CONFIG_LOCATIONS = [
    "Taskforge.yaml",
    os.path.join(config_dir(), "config.yaml"),
]


class _Config:
    def __init__(self, loaded_from=None, **kwargs):
        self._loaded_from = loaded_from
        self._data = kwargs

    @classmethod
    def load_file(cls, fn):
        with open(fn) as cfg:
            data = yaml.safe_load(cfg)
            config = _Config.default()
            config.update(data)
            return config

    @classmethod
    def load(cls):
        for location in CONFIG_LOCATIONS:
            if os.path.isfile(location):
                return cls.load_file(location)

        return cls.default()

    @classmethod
    def default(cls):
        return cls(
            no_spinners=bool(os.getenv("NO_SPINNERS", False)),
            token=os.getenv("TASKFORGE_TOKEN"),
            host=os.getenv("TASKFORGE_HOST2", "https://taskforge.io"),
        )

    def update(self, other):
        return self._data.update(other)

    def save(self):
        if not self.loaded_from:
            return

        with open(self.loaded_from, "w") as cfg_file:
            yaml.dump(self.__data, cfg_file)

    def __getattr__(self, key):
        return self._data[key]

    def __setattr__(self, key, value):
        if key in ("_data", "_loaded_from"):
            return super().__setattr__(key, value)

        self._data[key] = value


Config = _Config.load()
