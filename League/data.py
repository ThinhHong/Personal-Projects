import pandas as pd
import numpy as np
import sys
import configparser
import requests
import json
import time
import seaborn as sns
from mysql.connector import connect, Error

config = configparser.ConfigParser()
try:
    config.read('configlol.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

start_date = config['userID']['startDate']
my_host = config['userID']['host']
my_username = config['userID']['username']
my_password = config['userID']['password']
my_database = config['userID']['database']
api_key = config['userID']['apiKey']
summoner = config['userID']['intialSummoner']
by_name = config['userID']['by_name']
by_account = config['userID']['by_account']
by_puuid = config['userID']['by_puuid']
by_summoner = config['userID']['by_summoner']
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
high_tier =["MASTER","GRANDMASTER","CHALLENGER"]
division =["I","II","III","IV"]


class RiotApi:
      
      def __init__(self,api_key,region_match = "americas",region_player = "na1",queue = "RANKED_SOLO_5x5") -> None:
            self.api_key = api_key
            self.region_match = region_match
            self.region_player = region_player
            self.queue = queue
            print(f"Created RiotApi with api key: {api_key},matches in region :{region_match},player in {region_player}")

      def get_summoner_info_id(self,id):
            time.sleep(1.5)
            try:
                  http = (summoner + id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      

      def get_summoner_info_account_id(self,account_id):
            time.sleep(1.5)
            try:
                  http = (summoner + by_account + account_id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_puuid(self,puuid):
            time.sleep(1.5)
            try:
                  http = (summoner + by_puuid + puuid + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  time.sleep(2)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
   

      def get_summoner_info_name(self,summoner_name):
            time.sleep(1.5)
            try:
                  http = (summoner + by_name + summoner_name + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
      
      @staticmethod
      def insert_query(connection,data,table,rollback_on_error=True):
            values = ""
            for item in data.values():
                  if isinstance(item,str):
                        values = f'{values}"{item}",'
                  elif isinstance(item,int): 
                        if item > 22147483647:
                              values = f'{values}"{str(item)}",'
                        else:
                              values = f'{values}{item},'

                  elif item == True:
                         values = f'{values}"1",'
                              
                  elif item == False:
                         values = f'{values}"0",'

            values = f"({values[:-1]})"
            query = f"INSERT IGNORE INTO {table} VALUES {values}"
            print(query)
            try:
                  with connection.cursor() as cursor:
                        cursor.execute(query)
                        if not rollback_on_error:
                              connection.commit()
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise      

            
            
      @classmethod
      def insert_query_list(cls,connection,data,table):
            try:
                  if isinstance(data,list):
                        for item in data:
                              cls.insert_query(connection,item,table)

                  else:
                        cls.insert_query(connection,data,table)
            except Error as e:
                  print(f"Error: {e}")
                 
      @classmethod
      def insert_query_user(cls,connection,data):       
            cls.insert_query(connection,data,"player")

     
      @staticmethod
      def get_champion():
            try:
                  return requests.get(champions).json()
            
            except Exception as e:
                  print(f'Could not get values {e}')

      @staticmethod
      def get_stats(list):
            stats = ""
            for item in list.values():
                  stats = f"{stats},{item}"
            return stats[1:]
      
      @classmethod
      def insert_champions(cls,connection,champions):
            version = champions["version"]
            data = champions['data']
            columns = f"(champion_id,champion_name,version,attack,defense,magic,difficulty)"
            try:
                  with connection.cursor() as cursor:
                        for item, key in data.items():
                              stats = cls.get_stats(key['info'])
                              values = f"({key['key']},'{item}','{version}',{stats})"
                              query = f"INSERT INTO champion {columns} VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
                              cls.insert_type(connection,key['key'],key['tags'])
            except Error as e:
                  print(f"Error: {e}")

      @staticmethod
      def insert_type(connection,id,type):
            columns ="(tags,champion_id)"
            try:
                  with connection.cursor() as cursor:
                        for tag in type:
                              print(type)
                              values = f'("{tag}",{id})'
                              query = f"INSERT INTO type {columns} VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()

            except Error as e:
                  print(f"Error: {e}")

      @staticmethod
      def get_items():
            try:
                  return requests.get(items).json()
            
            except Exception as e:
                  print(f'Could not get values {e}')

      @staticmethod
      def insert_items(connection,items):
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
                                    connection.commit()
            
            except Error as e:
                  print(f'Could not insert query {e}')
                  
      
      def get_mastery(self,player):
            time.sleep(1.5)
            try:
                  http = (mastery + player['id'] + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
                  

      def get_mastery_champ(self,player,champ_id):
            time.sleep(1.5)
            try:
                  http = (mastery + player['id'] + by_champion + str(champ_id) + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  print(http)
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')


      @classmethod
      def insert_mastery(cls,connection,data):
           cls.insert_query(connection,data,"mastery")
            

      @classmethod
      def insert_all_mastery(cls,connection,data):
            cls.insert_query_list(connection,data,"mastery")
            
      
      @staticmethod
      def num_roman(num):
            
            roman = {1:'I',2:'II',3:'III',4:'IV'}
            return roman[num]


      def get_player_rank(self,player):
            time.sleep(1.5)
            http = (rank + by_summoner + player['id'] + query + self.api_key).format(
                  regionPlayer=self.region_player)
            
            print(http)
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_rank(self,tier,division):
            time.sleep(1.5)
            if isinstance(division,int):
                  division = self.num_roman(division)
            http = (rank +self.queue+'/' +tier +'/' + division+ query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            print(http)
            try:
                  return requests.get(http).json()
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
       
      
      def insert_rank(self,connection,data):
            for item in data:
                  values = ""
                  player = self.get_summoner_info_id(item['summonerId'])
                  self.insert_query_user(connection,player)
                  for key,value in item.items():
                        if value == True:
                              item[key] = 1
                        elif value == False:
                              item[key] = 0
                  
                  values = f"'{item['leagueId']}','{item['queueType']}','{item['tier']}','{item['rank']}','{player['id']}','{player['accountId']}','{player['puuid']}','{player['name']}',{item['leaguePoints']},{item['wins']},{item['losses']},{item['veteran']},{item['inactive']},{item['freshBlood']},{item['hotStreak']},"
                  values = f"({values[:-1]})"
                  query = f"INSERT INTO ranked VALUES {values}"
                  print(query)
                  try:
                        with connection.cursor() as cursor:
                              cursor.execute(query)
                              connection.commit()
                  except Error as e:
                        print(f"Error: {e}")  
             
      def insert_high_rank(self,connection,data):
            values = f'''"{data['leagueId']}","{data['queue']}","{data['tier']}"'''
            try:
                  for entry in data['entries']:
                        player = self.get_summoner_info_id(entry['summonerId'])
                        self.insert_query_user(connection,player)
                        for key,value in entry.items():
                              if value == True:
                                    entry[key] = 1
                              elif value == False:
                                    entry[key] = 0
                        
                        new_values = f"""{values},"{entry['rank']}","{player['id']}","{player['accountId']}","{player['puuid']}","{player['name']}",{entry['leaguePoints']},{entry['wins']},{entry['losses']},{entry['veteran']},{entry['inactive']},{entry['freshBlood']},{entry['hotStreak']},"""
                        new_values = f"({new_values[:-1]})"
                        query = f"INSERT INTO ranked VALUES {new_values}"
                        print(query)
                        try:
                              with connection.cursor() as cursor:
                                    cursor.execute(query)
                                    connection.commit()
                        except Error as e:
                              print(f"Error: {e}")  

            except Error as e:
                  print(f"Error: {e}")  

      


      def get_match_history_player(self,player,start=0,count=20):

            time.sleep(1.5)
            range = f"/ids?start={start}&count={count}" 
            http = (match + match_history + player['puuid'] + range + find + self.api_key).format(
                 
                  regionMatch=self.region_match
            )
            print(http)
            print(f"Getting match history from {start} to {count} games ago")
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')
   
      def get_match_history_puuid(self,puuid,start=0,count=20):
      
            time.sleep(1.5)    
            range = f"/ids?start={start}&count={count}" 
            http = (match + match_history + puuid + range + find + self.api_key).format(
                 
                  regionMatch=self.region_match
            )
            print(http)
            print(f"Getting match history from {start} to {count} games ago")
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')
      @staticmethod
      def insert_match_history(connection,user,match_history):
            try:
                  with connection.cursor() as cursor:
                        for item in match_history:
                              values = f"('{item}','{user['id']}','{user['accountId']}','{user['puuid']}','{user['name']}')"
                              query = f"INSERT INTO match_history VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
            except Error as e:
                  print(f"Error: {e}")

      @staticmethod
      def insert_match_history_data(connection,id,account_id,puuid,name,match_history):
            try:
                  with connection.cursor() as cursor:
                        for item in match_history:
                              values = f"('{item}','{id}','{account_id}','{puuid}','{name}')"
                              query = f"INSERT INTO match_history VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
            except Error as e:
                  print(f"Error: {e}")


                  
      def get_match(self,match_id):
            time.sleep(1.5)
            http = (match + match_details + match_id + query + self.api_key).format(
                  regionMatch=self.region_match
            )
            print(http)
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      
      def insert_participate (self,connection,participant,match_id):
            
            for key,value in participant.items():
                  if value == True :
                        participant[key] = 1
                  elif value == False:
                        participant[key] = 0
            
            values = f"""'{match_id}',{participant['assists']},{participant['champLevel']},{participant['championId']},'{participant['championName']}',{participant['damageDealtToTurrets']},
            {participant['deaths']},{participant['firstBloodKill']},{participant['firstTowerKill']},{participant['goldSpent']},{participant['item0']},{participant['item1']},
            {participant['item2']},{participant['item3']},{participant['item4']},{participant['item5']},{participant['item6']},{participant['kills']},
            {participant['participantId']},{participant['summonerLevel']},'{participant['summonerId']}','{participant['teamPosition']}',{participant['totalDamageDealtToChampions']},{participant['totalDamageTaken']},
            {participant['totalMinionsKilled']},{participant['turretTakedowns']},{participant['win']}
            """
            values = f"({values})"
            query = f"INSERT INTO participant VALUES {values}"
            print(query)
            try:
                  with connection.cursor() as cursor:
                        cursor.execute(query)
                        connection.commit()

            except Error as e:
                  print(f"Error has occured : {e}")

      def insert_match (self,connection,match):
            data = match['metadata']
            values = f"'{data['matchId']}','{data['dataVersion']}'"
            info = match['info']
            values = f"{values},{info['gameDuration']},'{info['gameId']}','{info['gameMode']}','{info['gameVersion']}',{info['mapId']},'{self.region_match}'"
            values = f"({values})"
            query = f"INSERT INTO game VALUES {values}"
      
            try:

                  with connection.cursor() as cursor:
                        print(query)
                        cursor.execute(query)
                        connection.commit()

                  for user in data['participants']:
                        player = self.get_summoner_info_puuid(user)
                        self.insert_query_user(connection,player)

                  for participant in info['participants']:
                        self.insert_participate(connection,participant,data['matchId'])

            except Error as e:
                  print(f"Error has occured : {e}")

      def insert_match_list(self,connection,match_history):
            for match_id in match_history:
                  match = self.get_match(match_id)
                  self.insert_match(connection,match)


      def insert_rank_history_sql(self,connection,tier,division,start=0,count=20):
            if isinstance(division,int):
                  division = self.num_roman(division)
            try:
                  with connection.cursor(buffered=True) as cursor:
                        query = f"SELECT ranked.puuid FROM ranked WHERE ranked.tier = '{tier}' AND ranked.division = '{division}'"
                        print(query)
                        cursor.execute(query)
                        players = cursor.fetchall()
                        for item in players:
                              player = self.get_summoner_info_puuid(item[0])
                              self.insert_query_user(connection,player)
                              history = self.get_match_history_puuid(item[0],start,count)
                              for match in history:
                                    game = self.get_match(match)
                                    self.insert_match(connection,game)

                              self.insert_match_history(connection,player,history)
      

            except Exception as e:
                  print(f'Could not make request {e}')

      @staticmethod
      def get_winrate_player(connection,player):
            try:
                  with connection.cursor(buffered = True) as cursor:
                        wins = f"SELECT COUNT(participant.id) AS id FROM participant WHERE participant.id = '{player['id']}' AND participant.win = 1"
                        games_played = f"SELECT COUNT(participant.id) FROM participant WHERE participant.id = '{player['id']}'"
                        print(wins)
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()
                        print(games_played)
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()
                        print(f"Player: {player['name']} has a win rate of {total_wins[0]*100/total_games[0]}% in {total_games[0]} games played ")
                        return total_games,(total_wins[0]/total_games[0])
                        

            except Error as e:
                  print(f"Error has occured : {e}")

      @staticmethod
      def get_winrate_champion(connection,champion):
            try:
                  with connection.cursor(buffered = True) as cursor:
                        wins = f"SELECT COUNT(participant.win) FROM participant WHERE participant.champion_name = '{champion}' AND participant.win = 1"
                        games_played = f"SELECT COUNT(participant.champion_name) FROM participant WHERE participant.champion_name = '{champion}'"
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()
                        print(f"Champion: {champion} has a win rate of {total_wins[0]*100/total_games[0]} % in {total_games[0]} games played")
                        return total_games,(total_wins[0]/total_games[0])
                        

            except Error as e:
                  print(f"Error has occured : {e}")
            
      

      @staticmethod
      def join(connection,join1,join2):
            try:
                  with connection.cursor(buffered=True) as cursor:
                        champions = f"SELECT "

            except Error as e:
                  print(f"Error has occured: {e}")
            

      @staticmethod
      def get_winrate_champion_rank(connection,champion,rank,division):
            try:
                  with connection.cursor(buffered = True) as cursor:
                        wins = f"""
                        SELECT COUNT(participant.win)
                        FROM participant
                        INNER JOIN ranked 
                        ON participant.id = ranked.id
                        WHERE participant.id = ranked.id AND participant.champion_name = '{champion}' AND ranked.tier = '{rank}' AND ranked.division = '{division}' AND participant.win = 1
                        """
                        games_played = f"""
                        SELECT COUNT(participant.win)
                        FROM participant
                        INNER JOIN ranked 
                        ON participant.id = ranked.id
                        WHERE participant.id = ranked.id AND participant.champion_name = '{champion}' AND ranked.tier = '{rank}' AND ranked.division = '{division}'
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()
                        print(f"Champion: {champion} has a win rate of {total_wins[0]*100/total_games[0]}% in {total_games[0]} games played at the rank {rank}")
                        return total_games,(total_wins[0]/total_games[0])
                        

            except Error as e:
                  print(f"Error has occured : {e}")


      @staticmethod
      def get_win_rate_item(connection,item):

            try:
                  with connection.cursor(buffered = True) as cursor:
                        if isinstance(item,str):
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name = item
                              item_id = cursor.fetchone()[0]
                        else:
                              item_id = item
                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.win = 1
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant as p
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()
                        cursor.execute(times_played)
                        total_participants = cursor.fetchone()
                        print(f"Item:{item_name} has a win rate of {total_wins[0]*100/total_games_item[0]}% in {total_games_item[0]} games played with a buy rate of {total_games_item[0]*100/total_participants[0]}%")
                        return total_games_item,(total_wins[0]/total_games_item[0])
                        
            except Error as e:
                  print(f"Error has occured : {e}")

              
      @staticmethod

      def get_win_rate_champion_mastery(connection,champion,item):
            try:
                  with connection.cursor(buffered = True) as cursor:
                        
                        if isinstance(item,str):
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name = item
                              item_id = cursor.fetchone()[0]
                        else:
                              item_id = item

                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.win = 1 AND p.champion_name = '{champion}'
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id} AND p.champion_name = '{champion}'
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant as p
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()
                        cursor.execute(times_played)
                        total_participants = cursor.fetchone()
                        print(f"Item:{item_name} has a win rate of {total_wins[0]*100/total_games_item[0]}% in {total_games_item[0]} games played with a buy rate of {total_games_item[0]*100/total_participants[0]}% playing{champion}")
                        return total_games_item,(total_wins[0]/total_games_item[0])
                        
            except Error as e:
                  print(f"Error has occured : {e}")


      def analyze(data):
           s =3 


      @staticmethod
      def execute_multiple_statements(connection, statements, rollback_on_error=True):
            try:
                  cursor = connection.cursor()
                  for statement in statements:
                        cursor.execute(statement)
                        if not rollback_on_error:
                              connection.commit() # commit on each statement
            except Exception as e:
                  print(f"Error has occured : {e}")
                  if rollback_on_error:
                        connection.rollback()
                  raise
            else:
                  if rollback_on_error:
                        connection.commit()


naServer = RiotApi(api_key,"americas","na1")
item = naServer.get_items()
mo = naServer.get_summoner_info_name("moman1898")
try:
      with connect(
            host= my_host,
            user= my_username,
            password= my_password,
            database = my_database,
      ) as connection:
            print(f"Connection {connection}")
      
            naServer.get_win_rate_item(connection,"bloodthirster")
            

except Error as e:
      print(f"Error: {e}")
