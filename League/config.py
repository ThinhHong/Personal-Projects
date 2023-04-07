import configparser
from datetime import datetime

config = configparser.ConfigParser()

#Sets the config dictionary
config["userID"] = {
    "startDate" : datetime.today().strftime('%Y-%m-%d'),
    "host" : "localhost",
    "username" : "root",
    "password" : "Pokemon25",
    "database" : "leagueoflegends",
    "apiKey" : "RGAPI-e6d650d1-ac36-41c5-94a4-6fca21e8f679",
    "intialSummoner" : "https://{regionPlayer}.api.riotgames.com/lol/summoner/v4/summoners/",
    "by_name" : "by-name/",
    "by_account" : "by-account/",
    "by_puuid" : "by-puuid/",
    "initialRank" :"https://na1.api.riotgames.com/lol/league/v4/entries/",
    "by_summoner" :"by-summoner/",
    "initialPlayer" : "https://{regionPlayer}.api.riotgames.com/lol/league/v4/",
    "masterPlayers":"masterleagues/by-queue/",
    "grandmasterPlayers" : "grandmasterleagues/by-queue/",
    "challengerPlayers" : "challengerleagues/by-queue/",
    "initialMastery" : "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/",
    "byChampion" : "/by-champion/",
    "initialMatch" : "https://{regionMatch}.api.riotgames.com/lol/match/v5/",
    "matchHistoryPuuid" : "matches/by-puuid/",
    "matchDetailsMatchID" : "matches/",
    "champions" : "http://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/champion.json",
    "items" : "http://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/item.json"
   
}

#creates a config file named configlol.ini
with open("configlol.ini","w") as f:
    """
    Creates a configuration file ncaleld configlol.ini
    Example usage:
        >>> config = read_config('config.ini')
    """
    config.write(f)
