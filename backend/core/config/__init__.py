import os

from pytz import timezone
from revolver_api.revolver_api.config import readTomlConfig,get as config_get  # noqa: F403
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = readTomlConfig(BASE_DIR / "config.toml")
assert config is not None

def get(key, default=None):
    return config_get(config, key, default)


tempDir = "tmp"
if not os.path.exists(tempDir):
    os.mkdir(tempDir)


def cache_dir(suffix=""):
    """_summary_

    Returns:
        _type_: _description_
    """
    path = get("cache.dir", "tmp")
    real_path = BASE_DIR / path
    if suffix is not None and suffix != "":
        real_path = real_path / suffix
    if not os.path.exists(real_path):
        os.mkdir(real_path)
    return real_path


def get_cache_file(name):
    """_summary_

    Args:
        name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return cache_dir() / name


TIME_ZONE = get("timezone.timezone")
DATETIME_FORMAT = get("timezone.datetime_format")
tz = timezone(TIME_ZONE)
