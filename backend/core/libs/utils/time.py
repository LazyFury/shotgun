
import datetime
import re
from pytz import timezone
from core import config


def toUtcTime(time)->str:
    return time.astimezone(timezone('UTC')).strftime(config.DATETIME_FORMAT)

def toLocalTime(time)->str:
    return time.astimezone(config.tz).strftime(config.DATETIME_FORMAT)

def isMatchTimeFormat(time_str)->bool:
    return re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", time_str)

