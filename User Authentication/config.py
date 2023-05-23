import configparser
import os
from datetime import datetime

config = configparser.ConfigParser()
cwd = os.getcwd()
os.chdir(cwd)

#Sets the config dictionary
config["user_database"] = {
    "startDate" : datetime.today().strftime('%Y-%m-%d'),
    "host" : "localhost",
    "username" : "root",
    "password" : "Pokemon25",
    "database" : "account",
 
}

#creates a config file named configlol.ini
with open("config_users.ini","w") as f:
    """
    Creates a configuration file ncaleld config_account.ini
    Example usage:
        >>> config = read_config('config.ini')
    """
    config.write(f)