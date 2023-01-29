import configparser
from datetime import datetime
from mysql.connector import connect, Error
import mysql.connector

config = configparser.ConfigParser()

config["userID"] = {
    "startDate" : datetime.today().strftime('%Y-%m-%d'),
    "intialSummoner" : "https://{regionPlayer}.api.riotgames.com/lol/summoner/v4/",
    "summonerNameApi" : "summoners/by-name/",
    "initialPLayer" : "https://{regionPlayer}.api.riotgames.com/lol/league/v4/",
    "masterPlayers":"masterleagues/by-queue/",
    "grandmasterPlayers" : "grandmasterleagues/by-queue/",
    "challengerPlayers" : "challengerleagues/by-queue/",
    "initialMatch" : "https://{regionMatch}.api.riotgames.com/lol/match/v5/",
    "matchHistoryPuuid" : "matches/by-puuid/",
    "matchDetailsMatchID" : "matches/",
    "username" : "root",
    "password" : "Pokemon25",
    "server" : "localhost",
    "database" : "leagueoflegends",
    "champions" : "http://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/champion.json",
    "items" : "http://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/item.json"
}

with open("configlol.ini","w") as f:
    config.write(f)

