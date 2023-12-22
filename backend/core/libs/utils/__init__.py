

import datetime
import re

from django.http import QueryDict

from core.libs.utils.time import toUtcTime


def func1():
    pass


def queryDictToDict(queryDict:QueryDict):
    """
    将QueryDict转换为dict
    :param queryDict: QueryDict
    :return: dict
    """
    result = queryDict.dict()
    for key in result:
        # if regxp match datetime str
        # is a datetime str 
        if isinstance(result[key], str):
            if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", result[key]):
                print("match", result[key])
                try:
                    t = datetime.datetime.strptime(result[key], "%Y-%m-%d %H:%M:%S")
                    result[key] = t.astimezone(datetime.timezone.utc)
                except ValueError:
                    pass
            
    print("queryDictToDict", result)
    return result