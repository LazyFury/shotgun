
from pathlib import Path

from pytz import timezone



BASE_DIR = Path(__file__).resolve().parent.parent.parent

def readTomlConfig():
    import toml
    
    configPath = str(BASE_DIR) + "/config.toml"
    
    # if file exits 
    if not Path(configPath).is_file():
        with open(configPath, "w") as f:
            f.write("[timezone]\ntimezone = \"Asia/Shanghai\"\ndatetime_format = \"%Y-%m-%d %H:%M:%S\"")
        raise Exception("config.toml not found,try to create a new one")
    
    with open(configPath, "r") as f:
        config = toml.load(f)
    return config

config = readTomlConfig()
print("read from config.toml ..." + config.__str__())


TIME_ZONE = config["timezone"]["timezone"]
DATETIME_FORMAT = config["timezone"]["datetime_format"]
tz = timezone(TIME_ZONE)