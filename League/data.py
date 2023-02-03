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
by_name = config['userID']['by_name']
by_id = config['userID']['by_id']
by_puuid = config['userID']['by_puuid']
match_history = config['userID']['matchHistoryPuuid']
match_details = config['userID']['matchDetailsMatchID']
match = config['userID']['initialMatch']
match_history = config['userID']['matchHistoryPuuid']
match_details = config['userID']['matchDetailsMatchID']
rank = config['userID']['initialRank']
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
champions = config['userID']['champions']
items = config['userID']['items']
mastery = config['userID']['initialMastery']
by_champion = config['userID']['byChampion']
match_regions = ["sea","asia","americas","europe"]
player_regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2"]
queue = ["RANKED_SOLO_5x5","RANKED_FLEX_SR","RANKED_FLEX_TT"]
tier = ["IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND"]
division =["I","II","III","IV"]


class RiotApi:
      
      
      def __init__(self,api_key,region_match = "americas",region_player = "na1",queue = "RANKED_SOLO_5x5") -> None:
            self.api_key = api_key
            self.region_match = region_match
            self.region_player = region_player
            self.queue = queue

     

      def get_summoner_info_name(self,summoner_name):
            try:
                  http = (summoner + by_name + summoner_name + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_id(self,id):
            try:
                  http = (summoner + by_id + id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )

                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_summoner_id(self,summoner_id):
            try:
                  http = (summoner + summoner_id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_puuid(self,puuid):

            try:
                  http = (summoner + by_puuid + puuid + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
   

      def insert_query_user(self,connection,data,):
            values = ""
            for key,item in data.items():
                  if isinstance(item,str):
                        values = f'{values}"{item}",'
                  elif isinstance(item,int):
                        if item > 22147483647:
                              values = f'{values}"{str(item)}",'
                        else:
                              values = f'{values}{item},'
            values = f"({values}'{self.region_player}')"
            query = f"INSERT INTO player VALUES {values}"
            print(query)
            try:
                  with connection.cursor() as cursor:
                        cursor.execute(query)
                        connection.commit()
            except Error as e:
                  print(f"Error: {e}")

      def insert_query(self,connection,data,table):
            values = ""
            for item in data.values():
                  if isinstance(item,str):
                        values = f'{values}"{item}",'
                  elif isinstance(item,int):
                        if item > 22147483647:
                              values = f'{values}"{str(item)}",'
                        else:
                              values = f'{values}{item},'
            values = f"({values[:-1]})"
            query = f"INSERT INTO {table} VALUES {values}"
            print(query)
            try:
                  with connection.cursor() as cursor:
                        cursor.execute(query)
                        connection.commit()
            except Error as e:
                  print(f"Error: {e}")            

      
      def insert_query_list(self,connection,data,table):
            try:
                  for item in data:
                        self.insert_query_user(connection,item,table)

            except Error as e:
                  print(f"Error: {e}")
            
      
      def get_match_history_id (self,puuid,start=0,count=20):

            time = f"/ids?start={start}&count={count}" 
            http = (match + match_history + puuid + time + find + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')
   


      def insert_match_history(self,connection,user,match_history):
            try:
                  with connection.cursor() as cursor:
                        for item in match_history:
                              values = f"('{item}','{user['id']}','{user['accountId']}','{user['puuid']}','{user['name']}')"
                              print(values)
                              query = f"INSERT INTO match_history VALUES {values}"
                              cursor.execute(query)
                              connection.commit()
            except Error as e:
                  print(f"Error: {e}")
            

      def get_match(self,match_id):
            http = (match + match_details + match_id + query + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')
  

      def get_item_champion(self,url):
            try:
                  return requests.get(url).json()
            
            except Exception as e:
                  print(f'Could not get values {e}')

      def insert_items(self,connection,items):
            columns = f"(item_id,item_name)"
            data = items['data']
            try:
                  with connection.cursor() as cursor:
                        for item, key in data.items():
                              if len(key["name"]) < 30:
                                    values = f'({item},"{key["name"]}")'
                                    query = f"INSERT INTO items {columns} VALUES {values}"
                                    print(query)
                                    cursor.execute(query)
            except Error as e:
                  print(f"Error: {e}")

      def insert_champions(self,connection,champions):
            version = champions["version"]
            data = champions['data']
            columns = f"(champion_id,champ_name,version,attack,defense,magic,difficulty)"
            try:
                  with connection.cursor() as cursor:
                        for item, key in data.items():
                              stats = self.get_stats(key['info'])
                              values = f"({key['key']},'{item}','{version}',{stats})"
                              query = f"INSERT INTO champions {columns} VALUES {values}"
                              cursor.execute(query)
                              connection.commit()
                              self.insert_type(connection,key['key'],key['tags'],"type")
            except Error as e:
                  print(f"Error: {e}")

      def insert_type(connection,id,type,table):
            columns ="(tags,champion_id)"
            try:
                  with connection.cursor() as cursor:
                        for tag in type:
                              print(type)
                              values = f'("{tag}",{id})'
                              query = f"INSERT INTO champion {columns} VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()

            except Error as e:
                  print(f"Error: {e}")

      def get_stats(list):
            stats = ""
            for item in list.values():
                  stats = f"{stats},{item}"
            return stats[1:]
      

      def get_mastery(self,id):

            try:
                  http = (mastery + id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
                  

      def get_mastery_champ(self,id,champ_id):

            try:
                  http = (mastery + id + by_champion + str(champ_id) + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def insert_query_mastery(self,connection,data,table):
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
            values = f"({values}'{self.region_player}')"
            query = f"INSERT INTO {table} VALUES {values}"
            print(query)
            try:
                  with connection.cursor() as cursor:
                        cursor.execute(query)
                        connection.commit()
            except Error as e:
                  print(f"Error: {e}")

      
            
      
      def get_rank(self,tier,division):

            http = (rank +self.queue+'/' +tier +'/' + division+ query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            print(http)
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def insert_rank(self,connection,rank):
            
            for item in rank:
                   self.insert_query_user(connection,self.get_summoner_info_id(item['summonerId']))


      
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
       

naServer = RiotApi(api_key,"americas","na1")
rank = naServer.get_rank("DIAMOND","I")
print(rank[0]["summonerId"])



try:
      with connect(
            host= 'localhost',
            user= 'root',
            password= 'Pokemon25',
            database = 'leagueoflegends',
      ) as connection:
            print(f"ConnectionL {connection}")
            naServer.insert_rank(connection,rank)
            
            

except Error as e:
      print(f"Error: {e}")
