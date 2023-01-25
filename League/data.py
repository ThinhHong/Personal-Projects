import pandas as pd
import numpy as np
import sys
import configparser
import requests
import json
import decimal
import mysql.connector
from mysql.connector import connect, Error
config = configparser.ConfigParser()
try:
    config.read('configlol.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

start_date = config['userID']['startDate']
summoner = config['userID']['intialSummoner']
summoner_name_api = config['userID']['summonerNameApi']
match_history = config['userID']['matchHistoryPuuid']
match_details = config['userID']['matchDetailsMatchID']
match = config['userID']['initialMatch']
match_history = config['userID']['matchHistoryPuuid']
match_details = config['userID']['matchDetailsMatchID']
players = config['userID']['initialPlayer']
master_players = config['userID']['masterPlayers']
grandmaster_players = config['userID']['masterPlayers']
challenger_players = config['userID']['challengerPlayers']
my_server = config['userID']['server']
test_database = config['userID']['database']
api_key = config['userID']['apiKey']
my_user = config['userID']['username']
my_password = config['userID']['password']
query = "?api_key="
find = "&api_key="

match_regions = ["sea","asia","americas","europe"]
player_regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2"]
queue = ["RANKED_SOLO_5x5","RANKED_FLEX_SR","RANKED_FLEX_TT"]

class RiotApi:
      
     
      def __init__(self,api_key,region_match = "americas",region_player = "na1",queue = "RANKED_SOLO_5x5") -> None:
            self.api_key = api_key
            self.region_match = region_match
            self.region_player = region_player
            self.queue = queue

      def get_summoner_info_name(self,summoner_name):
            try:
                  http = (summoner + summoner_name_api + summoner_name + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_puuid(self,puuid):

            try:
                  http = (summoner + summoner_name_api + puuid + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
   
                  
      def get_puuid(self,summoner_info):

            return (summoner_info['puuid'])
      
      def get_match_history_id (self,puuid,start=0,count=20):

            time = f"/ids?start={start}&count={count}" 
            http = (match + match_history + puuid + time + find + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')
   



      def get_match(self,match_id):
            http = (match + match_details + match_id + query + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  list = requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')
  
      
      
      def get_master(self):
            http = (players + master_players +self.queue+ query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_grandmaster(self):
            http = (players + grandmaster_players +self.queue+ query + self.api_key).format(
                  regionPlayer = self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not get values {e}')


      def get_challenger(self):
            http = (players + challenger_players +self.queue+ query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not get values {e}')



def insert_query_dictionary(connection,data,table):
      columns = ""
      values = ""
      for key,item in data.items():
            columns = f"{columns}{key},"
            if isinstance(item,str):
                  values = f'{values}"{item}",'
            elif isinstance(item,int):
                  if item > 22147483647:
                        values = f'{values}"{str(item)}",'
                  else:
                        values = f'{values}{item},'
      columns = f"({columns[:-1]})"
      values = f"({values[:-1]})"
      query = f"INSERT INTO {table} {columns} VALUES {values}"
      print(query)
      try:
            with connection.cursor() as cursor:
                  cursor.execute(query)
                  connection.commit()
      except Error as e:
            print(f"Error: {e}")

def insert_match            


naServer = RiotApi(api_key,"americas","na1")
name = naServer.get_summoner_info_name("moman1898")
puuid = naServer.get_puuid(name)
matchHistory = naServer.get_match_history_id(puuid)
challenger = naServer.get_challenger()


connection = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password= 'Pokemon25',
            database = 'leagueoflegends'

)

print(type(matchHistory[0]))

