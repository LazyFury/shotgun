import os
from pathlib import Path

from pytz import timezone
from requests import get


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def readTomlConfig():
    """_summary_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    import toml

    configPath = str(BASE_DIR) + "/config.toml"

    # if file exits
    if not Path(configPath).is_file():
        with open(configPath, "w") as f:
            f.write(
                '[timezone]\ntimezone = "Asia/Shanghai"\ndatetime_format = "%Y-%m-%d %H:%M:%S"'
            )
        raise Exception("config.toml not found,try to create a new one")

    with open(configPath, "r") as f:
        config = toml.load(f)
    return config


config = readTomlConfig()
print("read from config.toml ...")


def get(domain, default=""):  # noqa: F811
    """_summary_

    Args:
        domain (_type_): _description_
        default (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    keys = domain.split(".")
    target = config
    for key in keys:
        if key in target:
            target = target[key]
        else:
            return default
    return target


TIME_ZONE = get("timezone.timezone")
print("TIME_ZONE", TIME_ZONE)
DATETIME_FORMAT = get("timezone.datetime_format")
tz = timezone(TIME_ZONE)


def cacheDir():
    """_summary_

    Returns:
        _type_: _description_
    """
    path = get("cache.dir", "tmp")
    real_path = BASE_DIR / path
    if not os.path.exists(real_path):
        os.mkdir(real_path)
    return real_path


def cacheFile(name):
    """_summary_

    Args:
        name (_type_): _description_

    Returns:
        _type_: _description_
    """
    return cacheDir() / name
