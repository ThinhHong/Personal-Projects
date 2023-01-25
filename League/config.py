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
    "apiKey" : "RGAPI-7b258857-8def-4afa-b59b-9d9c74f86e24",
    "username" : "root",
    "password" : "Pokemon25",
    "server" : "localhost",
    "database" : "leagueoflegends"
}

with open("configlol.ini","w") as f:
    config.write(f)

connection = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password= 'Pokemon25',
            database = 'leagueoflegends'

)


try:
            query = f"""
            INSERT INTO user {columns}
            VALUES{values}
            """

            with connection.cursor() as cursor:
                  cursor.execute(query)
                  connection.commit()

      except Error as e:
            print(f"Error {e}")