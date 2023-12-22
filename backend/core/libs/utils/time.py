


from pytz import timezone
from core import config


def toUtcTime(time)->str:
    return time.astimezone(timezone('UTC')).strftime(config.DATETIME_FORMAT)

def toLocalTime(time)->str:
    return time.astimezone(config.tz).strftime(config.DATETIME_FORMAT)