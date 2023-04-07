import pandas as pd
import numpy as np
import sys
import configparser
import requests
import time
import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import connect, errorcode, Error

#Try to read config file
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
#All champion taken from data dragon website
champions = config['userID']['champions']
#All items taken from data dragon website
items = config['userID']['items']
mastery = config['userID']['initialMastery']
by_champion = config['userID']['byChampion']

"All region a match can take place in"
match_regions = ["sea","asia","americas","europe"]
"All region a player can exist in"
player_regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2"]
"All types of queues"
queue = ["RANKED_SOLO_5x5","RANKED_FLEX_SR","RANKED_FLEX_TT"]
"All types of tiers"
tier = ["IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND"]
"All types of high_tiers"
high_tier =["MASTER","GRANDMASTER","CHALLENGER"]
"All divisions"
division =["I","II","III","IV"]

class RiotAPI:
      """
      A class that represents the Riot API and its parameters.
      Parameters:
      api_key : str
      A string representing the API key used to access Riot API.
      match_region : str"
      A string representing the region of the match (e.g., match_regions = ["sea","asia","americas","europe"]
      player_region : str
      A string representing the region of the player (e.g., player_regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2"]
      queue_type : str
      A string representing the type of queue (e.g., queue = ["RANKED_SOLO_5x5","RANKED_FLEX_SR","RANKED_FLEX_TT"]
      """ 
      def __init__(self,api_key: str, region_match: str = "americas" , region_player: str = "na1", queue= "RANKED_SOLO_5x5") -> None:
            """
            Initializes a new RiotAPI instance with the provided parameters.
            Parameters:
            api_key : str
            A string representing a personal API key used to access Riot API represented as YOURAPIKEY.
            match_region : str
            A string representing the region of the match that is in one of the following ("sea","asia","americas","europe")
            player_region : str
            A string representing the region of the player that is in one of the following ("br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2").
            queue_type : str
            A string representing the type of queue that is one of the following ("RANKED_SOLO_5x5","RANKED_FLEX_SR","RANKED_FLEX_TT"]).
            """
            self.api_key = api_key
            self.region_match = region_match
            self.region_player = region_player
            self.queue = queue
            print(f"Created RiotApi with api key: {api_key},matches in region :{region_match},player in {region_player}")

      def get_summoner_info_id(self, id: str) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's info using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with a user's id and YOURAPIKEY
            Parameters:
            - id (str): A string representing the a User's summoner id to create an API endpoint to send the request to.
            Returns: A JSON object containing the response data that is converted into a dictionary.
            Example Usage:
            response = request.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/JBKCGB6vOqJuflnawS2PNM7rupJh15Q5TWACOj8okHpQKws?api_key=YOURAPIKEY')
            """
            time.sleep(1.5)
            try:
                  http = (summoner + id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_account_id(self, account_id: str) -> dict: 
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's info using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with a user's account id and YOURAPIKEY
            Parameters:
            - account_ad (str): A string representing the a User's account_id to create an API endpoint to send the request to.
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            time.sleep(1.5)
            try:
                  http = (summoner + by_account + account_id + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_summoner_info_puuid(self, puuid: str) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's info  using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with a user's puuid id and YOURAPIKEY
            Parameters:
            - puuid (str): A string representing the a User's account_id to create an API endpoint to send the request to.
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            time.sleep(1.5)
            try:
                  http = (summoner + by_puuid + puuid + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
   
      def get_summoner_info_name(self, summoner_name: str) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's info  using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with a user's name and YOURAPIKEY
            Parameters:
            name: A string representing the a User's account_id to create an API endpoint to send the request to.
            Returns:A JSON object containing the response data that is then converted into a dictonary.
            """
            time.sleep(1.5)
            try:
                  http = (summoner + by_name + summoner_name + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
      
      @staticmethod
      def insert_query(connection: connect, data: dict, table_name: str, rollback_on_error=False) -> None:
            """
            Inserts the provided query into an SQL table using the MySQL library. Function requires all values in dictonary to be needed in table
            Parameters:
            connection: MySQL connection
            A connection to a User's Database
            query : str
            A string representing the SQL query to be executed.
            data : dictionary
            A dictionary containing the data to be insertered. Integer values over 22147483647 are converted to strings as MySQL can not handle large intergers.
            table : str
            A string representing the name of the table into which the data will be inserted.
            Returns: None
            Errors: If there is an error connecting to the MySQL server or executing the query.
            """
            values = ""
            "Creates a long string with all values of dictionary into 1 string seperated by comma"
            for item in data.values():
                  if isinstance(item,str):
                        values = f'{values}"{item}",'
                  elif isinstance(item,int):
                        "Values over 221247483647 are not able to be proccsedd in sql and are converted to a string"
                        if item > 22147483647:
                              values = f'{values}"{str(item)}",'
                        else:
                              values = f'{values}{item},'

                  elif item == True:
                        "MySQL does not support boolean type. Values are changed into TINYINT in SQL. 1(True) or 0(False)"
                        values = f'{values}"1",'
                  elif item == False:
                         values = f'{values}"0",'

            values = f"({values[:-1]})"
            query = f"INSERT INTO {table_name} VALUES {values}"
            try:
                  with connection.cursor() as cursor:
                        print(query)
                        cursor.execute(query)
                        if not rollback_on_error:
                              connection.commit()

            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise      

      def insert_query_list(self, connection: connect, data: dict, table_name : str) -> None:
            """
            Inserts a list of queries into a table by calling insert_query for every item in list
            """
            try:
                  if isinstance(data,list):
                        for item in data:
                              self.insert_query(connection,item,table_name)
                  else:
                        self.insert_query(connection,data,table_name)

            except Error as e:
                  print(f"Error: {e}")
                 
      def insert_query_user(self, connection: connect, data: dict) -> None:
            """
            Inserts a user into table player by calling insert_query with table set to player.
            """       
            self.insert_query(connection,data,"player")
   
      @staticmethod
      def get_champion() -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to Data Dragon containing all current champions and returns the response in JSON format.
            Parameters:
            - None    
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            try:
                  return requests.get(champions).json()
            
            except Exception as e:
                  print(f'Could not get values {e}')

      @staticmethod
      def get_stats(list: list) -> None:
            """Description:
            This function takes a list of stats. It is called by insert_champions in order to seperate the champion file and append to 1 string
            Parameters:
            - list : A list containing the stats of a champions
            Returns: A str object containing the stats of a champion.
            """
            stats = ""
            for item in list.values():
                  stats = f"{stats},{item}"
            return stats[1:]
      
      @classmethod
      def insert_champions(cls,connection: connect, champions: dict) -> None:
            """
            Inserts all champions into SQl using the MySQL library. Extracts important information from champion JSON file.
            Parameters 
            connection: MySQL connection to a User's Database
            champions: a dictionary containing the all champions to be insertered. Integer values over 22147483647 are converted to strings as MySQL can not handle large intergers.
            Returns: None
            Error : If there is an error connecting to the MySQL server or executing the query.
            """
            version = champions["version"]
            data = champions['data']
            columns = f"(champion_id,champion_name,version,attack,defense,magic,difficulty)"
            try:
                  with connection.cursor() as cursor:
                        for item, key in data.items():
                              stats = cls.get_stats(key['info'])
                              # Appends all values from a champion json file into one string.
                              values = f"({key['key']},'{item}','{version}',{stats})"
                              query = f"INSERT INTO champion {columns} VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
                              cls.insert_type(connection,key['key'],key['tags'])
            except Error as e:
                  print(f"Error: {e}")

      @staticmethod
      def insert_type(connection: connect, champion_id: int, type: str) -> None:
            """
            Inserts a champinos type into SQl table named type using the MySQL library.
            Parameters
            connection: MySQL connection  A connection to a User's Database
            champion_id : int  A integer representing a champion
            type: list  A list containing all of a champion's type
            Returns: None
            Error If there is an error connecting to the MySQL server or executing the query.
            """
            columns ="(tags,champion_id)"
            try:
                  with connection.cursor() as cursor:
                        for tag in type:
                              print(type)
                              values = f'("{tag}",{champion_id})'
                              query = f"INSERT INTO type {columns} VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()

            except Error as e:
                  print(f"Error: {e}")

      @staticmethod
      def get_items() -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to Data Dragon containing all current items and returns the response in JSON format converted to dictionary.
            Parameters: None    
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            try:
                  return requests.get(items).json()
            
            except Exception as e:
                  print(f'Could not get values {e}')

      @staticmethod
      def insert_items(connection: connect, items: dict) -> None:
            """
            Inserts all items into SQl table items using the MySQL library.
            Parameters
            connection: MySQL connection to a User's Database
            items: dictionary containing the all items to be insertered. Strings containing more than 30 charecters are not inserted as they are not items
            Returns: None
            Error: If there is an error connecting to the MySQL server or executing the query.
            """
            columns = f"(item_id,item_name)"
            data = items['data']
            try:
                  with connection.cursor() as cursor:
                        for item, key in data.items():
                              if len(key["name"]) < 35:
                                    "Values of length over 35 are not items in leauge of legends and are not included"
                                    values = f'({item},"{key["name"]}")'
                                    query = f"INSERT INTO items {columns} VALUES {values}"
                                    print(query)
                                    cursor.execute(query)
                                    connection.commit()
            
            except Error as e:
                  print(f'Could not insert query {e}')
                  
      
      def get_mastery(self, player: dict) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's complete champion mastery using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and YOURAPIKEY
            Parameters:
            - player : A dictionary containing all of a User's info 
            Returns: A JSON object containing the response data that is then converted into a dictonary..
            """
            time.sleep(1.5)
            try:
                  http = (mastery + player['id'] + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')
                  

      def get_mastery_champ(self, player: dict, champ_id: int) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's specific champion mastery using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner, champ_id, query and YOURAPIKEY
            Parameters:
            - player : A dictionary containing all of a User's info 
            - champ_id : int champions specific id
            Returns: A JSON object containing the response data that is then converted into a dictonary..
            """
            time.sleep(1.5)
            try:
                  http = (mastery + player['id'] + by_champion + str(champ_id) + query + self.api_key).format(
                        regionPlayer=self.region_player
                  )
                  return requests.get(http).json()
            
            except Exception as e:
                  print(f'Could not make request {e}')


      @classmethod
      def insert_mastery(cls, connection: connect, data: dict) -> None:
            """
            Inserts a user's mastery into SQl using the MySQL library.
            Parameters:
            connection: MySQL connection
            A connection to a User's Database
            data : dictionary
            A dictinoary containing a specific champion mastery
            Returns:
            -------
            None
      
            Error
            If there is an error connecting to the MySQL server or executing the query.
            """
            cls.insert_query(connection,data,"mastery")
            

      @classmethod
      def insert_all_mastery(cls, connection: connect, data: dict) -> None:
            "Inserts A user's complete mastery page into an SQL table"
            cls.insert_query_list(connection,data,"mastery")
            
      def get_player_rank(self, player: dict) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's rank using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the query, player and YOURAPIKEY
            Parameters:
            - player : dictionary containing all of a User's info the a User's info
            Returns: A JSON object containing the response data that is then converted into a dictonary..
            """
            time.sleep(1.5)
            http = (rank + by_summoner + player['id'] + query + self.api_key).format(
                  regionPlayer=self.region_player
                  )         
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_player_rank_id(self, id: str) -> dict:
            """Description:
            Function is similar to get_player_rank excecpt it only requires a player's id
            """
            time.sleep(1.5)
            http = (rank + by_summoner + id + query + self.api_key).format(
                  regionPlayer=self.region_player
                  )         
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_rank(self, tier: str, division: str) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing all users in a tier and division using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the query, player and YOURAPIKEY
            Parameters:
            - tier : str representing one of 6 tiers ("IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND")
            - division : str representing one of 4 divisions ("I","II","III","IV")
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            time.sleep(1.5)
            http = (rank +self.queue+'/' +tier +'/' + division + query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_master(self) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing all players in the rank master using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the query, player and YOURAPIKEY
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            http = (players + master_players + self.queue + query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def get_grandmaster(self)-> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing all players in the rank grandmaster using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the query, player and YOURAPIKEY
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            http = (players + grandmaster_players +self.queue+ query + self.api_key).format(
                  regionPlayer = self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not get values {e}')

      def get_challenger(self)-> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing all players in the rank challenger using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the query, player and YOURAPIKEY
            Returns: A JSON object containing the response data that is then converted into a dictonary.
            """
            http = (players + challenger_players +self.queue+ query + self.api_key).format(
                  regionPlayer=self.region_player
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not get values {e}')
      def insert_rank(self, connection: connect, item: list, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a ranks information and all players in rank into an SQL database named ranked
            Parameters
            connection: MySQL connection to a User's Database
            item : dictionary containing a rank's and division's users ("IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND") tier, ("I","II","III","IV")
            Returns: None
            """
            try:  
                  with connection.cursor() as cursor:
                        #Converts boolean values to TINYINT for SQL database         
                        for key,value in item.items():
                              if value == True:
                                    item[key] = 1
                              elif value == False:
                                    item[key] = 0

                        "player_query is used to determine if user is already in database. "
                        player_query = f"SELECT EXISTS(SELECT * FROM player WHERE player.id = '{item['summonerId']}')"
                        cursor.execute(player_query)
                        exist = cursor.fetchone()[0]
                        "If user is not in database exist = 0 and the player is added to the database. Else their information is not required to get, Values changed to represent boolean"
                        values = ""
                        if exist == 0:
                              #Since player from rank json file is not in database, get_summoner_info_id and self.insert_query_user is used to retrieve and insert player
                              player = self.get_summoner_info_id(item['summonerId'])
                              self.insert_query_user(connection,player)
                              values = f"'{item['leagueId']}','{item['queueType']}','{item['tier']}','{item['rank']}','{player['id']}','{player['accountId']}','{player['puuid']}','{player['name']}',{item['leaguePoints']},{item['wins']},{item['losses']},{item['veteran']},{item['inactive']},{item['freshBlood']},{item['hotStreak']},"
                              values = f"({values[:-1]})"

                        else:
                              #Since user is in database, their data is retrieved to create a query to insert the rank table. This allows for fewer request using Riot's API to optimize run time due to the rate limits.
                              user_query = f"SELECT id,account_id,puuid,name FROM player WHERE player.id = '{item['summonerId']}'"
                              cursor.execute(user_query)
                              info = cursor.fetchone()
                              values = f"""'{item['leagueId']}','{item['queueType']}','{item['tier']}','{item['rank']}',"{info[0]}","{info[1]}","{info[2]}","{info[3]}",{item['leaguePoints']},{item['wins']},{item['losses']},{item['veteran']},{item['inactive']},{item['freshBlood']},{item['hotStreak']},"""
                              values = f"({values[:-1]})" 

                        query = f"INSERT INTO ranked VALUES {values}"
                        cursor.execute(query)

                        if not rollback_on_error:
                              connection.commit()
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise  
             
      def insert_player_rank(self, connection: connect, data: list, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a player's ranks information into an SQL database named ranked. Players can have a rank in Rank solo, rank flex, none or both. Data is obtained using get_rank
            Parameters:
             - connection: MySQL connection to a User's Database
             - data : dictionary containing a rank's and division's users ("IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND") tier, ("I","II","III","IV")
            Returns: None
            """
            #Using get_rank in to retrieve rank can return a list of varying size as the player can have different types of rank. len of either 0(no rank),1(1 type rank),2(both ranks)
            if len(data) == 0:
                  print("Player does not have a rank")
                  return

            print(type(data))                  
            for rank in data:
                  #The RiotAPI class is set to a specific queue. This if statements checks if the player has the correct rank queue type before inserting
                  if rank['queueType'] == self.queue:
                        self.insert_rank(connection,rank)

      def insert_all_rank(self, connection: connect, data: list, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a list of player's ranks information into an SQL database named ranked. This function can be used to insert all players in a rank using get_rank
            Parameters:
             - connection: MySQL connection to a User's Database
             - data : dictionary containing a rank's and division's users ("IRON","BRONZE","SILVER","GOLD","Platinium","DIAMOND") tier, ("I","II","III","IV")
            Returns: None
            """
            for item in data:
                  self.insert_rank(connection,item)

      def insert_high_rank(self, connection: connect, data: dict, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a ranks information into an SQL database named ranked. Similar to insert_rank_list function except high_ranks JSON files need to be processed differently
            Checks if user exist in database before inserting rank
            Parameters:
            connection: MySQL connection to a User's Database
            data : dictionary containing a high rank's user high_tier =["MASTER","GRANDMASTER","CHALLENGER"]
            Returns: None
            """
            values = f'''"{data['leagueId']}","{data['queue']}","{data['tier']}"'''
            print(values)
            try:
                  with connection.cursor() as cursor:
                        for entry in data['entries']:
                              for key,value in entry.items():
                                    if value == True:
                                          entry[key] = 1
                                    elif value == False:
                                          entry[key] = 0

                              #Using same queries to check for player in database as insert_rank. Used for the same optimization reasons
                              player_query = f"SELECT EXISTS(SELECT * FROM player WHERE player.id = '{entry['summonerId']}')"
                              cursor.execute(player_query)
                              exist = cursor.fetchone()[0]
                              if exist == 0:
                                    player = self.get_summoner_info_id(entry['summonerId'])
                                    self.insert_query_user(connection,player)
                                    new_values = f""" {values},"{entry['rank']}","{player['id']}","{player['accountId']}","{player['puuid']}","{player['name']}",{entry['leaguePoints']},{entry['wins']},{entry['losses']},{entry['veteran']},{entry['inactive']},{entry['freshBlood']},{entry['hotStreak']},"""
                                    new_values = f"({new_values[:-1]})"
                                    print(new_values) 
                              
                              else:
                                    user_query = f"SELECT id,account_id,puuid,name FROM player WHERE player.id = '{entry['summonerId']}'"
                                    cursor.execute(user_query)
                                    info = cursor.fetchone()
                                    new_values = f"""{values},"{entry['rank']}",'{info[0]}','{info[1]}','{info[2]}','{info[3]}',{entry['leaguePoints']},{entry['wins']},{entry['losses']},{entry['veteran']},{entry['inactive']},{entry['freshBlood']},{entry['hotStreak']},"""
                                    new_values = f"({new_values[:-1]})" 
                                    print(new_values) 

                              query = f"INSERT INTO ranked VALUES {new_values}"
                              print(query)
                              cursor.execute(query)
                              if not rollback_on_error:
                                    connection.commit()
                     
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise
             

      def insert_participant (self, connection: connect, participant: dict, match_id: str, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a participant from a match into  SQL database named match using MySQL connector
            Parameters:connection: MySQL connection
            A connection to a User's Database 
            participant : dictionary dictionary representing a particpate's data such as their kill and assist
            match_id : a str id represnting a match
            Return: None
            """
            for key,value in participant.items():
                  if value == True :
                        participant[key] = 1
                  elif value == False:
                        participant[key] = 0
            
            try:
                  with connection.cursor() as cursor:
                        item_list = []
                        for i in range (7):
                              #Appends all items 0-6 into 1 list with an items name
                              #items with value of 0 are not an item. They are converted to strong No item to represent the null value
                              if participant[f'item{i}'] == 0:
                                    item_list.append("No item")
                              else:
                                    #query is used to retrieve the items name for the SQL database in order to add to match table. match dictionary containing the data only has item id and not item_name
                                    query = f"SELECT items.item_name FROM items WHERE items.item_id = {participant[f'item{i}']}"
                                    cursor.execute(query)
                                    item_list.append(cursor.fetchone()[0])

                        values = f"""
                        "{match_id}",{participant['assists']},{participant['champLevel']},{participant['championId']},"{participant['championName']}",{participant['damageDealtToTurrets']},
                        {participant['deaths']},{participant['firstBloodKill']},{participant['firstTowerKill']},{participant['goldSpent']},{participant['item0']},{participant['item1']},
                        {participant['item2']},{participant['item3']},{participant['item4']},{participant['item5']},{participant['item6']},"{item_list[0]}","{item_list[1]}",
                        "{item_list[2]}","{item_list[3]}","{item_list[4]}","{item_list[5]}","{item_list[6]}",{participant['kills']},
                        {participant['participantId']},{participant['summonerLevel']},"{participant['summonerId']}","{participant['teamPosition']}",{participant['totalDamageDealtToChampions']},
                        {participant['totalDamageTaken']},{participant['totalMinionsKilled']},{participant['turretTakedowns']},{participant['win']}
                        """
                        values = f"({values})"
                        query = f"INSERT INTO participant VALUES {values}"
                        print(query)
                        cursor.execute(query)
                        connection.commit()
      
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise

      def get_match(self, match_id: str) -> dict:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing match data using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with match history, query and YOURAPIKEY
            Parameters: match_ id(str): A string representing a match id to create an API endpoint to send the request to.
            Returns: A JSON object containing the response data that is converted into a dictionary.
            """
            time.sleep(1.5)
            http = (match + match_details + match_id + query + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()
            except Exception as e:
                  print(f'Could not make request {e}')

      def insert_match(self, connection: connect, match: dict, rollback_on_error: bool=False) -> None:
            """Description:
            Inserts a participant from a match into  SQL database named match_details using MySQL connector
            Parameters 
            connection: A MySQL connection to a User's Database
            match: A dictionary contaiting a match data
            Return: None
            A match can also have people have different ranks
            so this function ensures any player not added in by insert_rank, is added here. Users can have the same match in their match history as well. Therefore it is needed to check
            if a match is already inserted.
            """  
            try:
                  with connection.cursor() as cursor:
                        data = match['metadata']
                        #Checks existence of match before retrieving the data. Used to optimize run time and SQL table by not readding existing data
                        history_query = f"SELECT EXISTS(SELECT * FROM game WHERE game.match_id = '{data['matchId']}')"
                        cursor.execute(history_query)
                        exist = cursor.fetchone()[0]
                        if exist == 1:
                              print("game already in")
                              #If the match is already in the SQL database, returns early
                              return
                        
                        "Appends values of a match into 1 string"
                        values = f"'{data['matchId']}','{data['dataVersion']}'"
                        info = match['info']
                        values = f"{values},{info['gameDuration']},'{info['gameId']}','{info['gameMode']}','{info['gameVersion']}',{info['mapId']},'{self.region_match}'"
                        values = f"({values})"
                        query = f"INSERT INTO game VALUES {values}"
                        print(query)
                        cursor.execute(query)
                        connection.commit()
                        for user in data['participants']:
                              player_query = f"SELECT EXISTS(SELECT * FROM player WHERE player.puuid = '{user}')"
                              cursor.execute(player_query)
                              exist = cursor.fetchone()[0]
                              print(exist + "1")
                              "If user is not in database, they are added in. Else their information is not required to get, Values changed to represent boolean"
                              #Using same queries to check for player in database as insert_rank. Used for the same optimization reasons
                              if exist == 0:
                                    player = self.get_summoner_info_puuid(user)
                                    self.insert_query_user(connection,player)
                                    player_rank = self.get_player_rank(player)
                                    self.insert_player_rank(player_rank)

                              else:
                                    "Checks if user's rank is inserted into the database already"
                                    rank_exist_query = f"SELECT EXISTS(SELECT * FROM ranked WHERE ranked.puuid = '{user}')"
                                    cursor.execute(rank_exist_query)
                                    exist = cursor.fetchone()[0]
                                    print(exist + "2")
                                    if exist == 0:
                                          rank_query = f"SELECT id FROM player WHERE player.puuid = '{user}'"
                                          cursor.exectue(rank_query)
                                          id = cursor.fetchone()[0]
                                          player_rank = self.get_player_rank_id(id)
                                          self.insert_player_rank(player_rank)   

                        for participant in info['participants']:
                              self.insert_participant(connection,participant,data['matchId'])
                        
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise

      def insert_match_id (self, connection: connect, match_id: str,rollback_on_error: bool=False) -> None:
            """Description:
            Function is similar to insert_match except it inserts a match using a match_id. 
            """ 
            try:
                  with connection.cursor() as cursor:
                        #Checks existence of match before retrieving the data. Used to optimize run time by reducing the amount of needed retrieves.
                        history_query = f"SELECT EXISTS(SELECT * FROM game WHERE game.match_id = '{match_id}')"
                        cursor.execute(history_query)
                        exist = cursor.fetchone()[0]
                        if exist == 1:
                              print("game already in")
                              return

                        match = self.get_match(match_id)
                        data = match['metadata']
                        values = f"'{data['matchId']}','{data['dataVersion']}'"
                        info = match['info']
                        values = f"{values},{info['gameDuration']},'{info['gameId']}','{info['gameMode']}','{info['gameVersion']}',{info['mapId']},'{self.region_match}'"
                        values = f"({values})"
                        query = f"INSERT INTO game VALUES {values}"
                        print(query)
                        cursor.execute(query)
                        connection.commit()
      
                        for user in data['participants']:
                              player_query = f"SELECT EXISTS(SELECT * FROM player WHERE player.puuid = '{user}')"
                              cursor.execute(player_query)
                              exist = cursor.fetchone()[0]
                              "If user is not in database, they are added in. Else their information is not required to get, Values changed to represent boolean"
                              #Using same queries to check for player in database as insert_rank. Used for the same optimization reasons
                              if exist == 0:
                                    player = self.get_summoner_info_puuid(user)
                                    self.insert_query_user(connection,player)
                                    player_rank = self.get_player_rank(player)
                                    self.insert_player_rank(connection,player_rank)

                              else:
                                    rank_exist_query = f"SELECT EXISTS(SELECT * FROM ranked WHERE ranked.puuid = '{user}')"
                                    cursor.execute(rank_exist_query)
                                    exist = cursor.fetchone()[0]
                                    if exist == 0:
                                          rank_query = f"SELECT id FROM player WHERE player.puuid = '{user}'"
                                          print(rank_query)
                                          cursor.execute(rank_query)
                                          player_rank = self.get_player_rank_id(id)
                                          self.insert_player_rank(connection,player_rank) 

                        print("stop")
                        for participant in info['participants']:
                              self.insert_participant(connection,participant,data['matchId'])
                        
            except Error as e:
                  print(f"Error has occured: {e}")
                  if rollback_on_error:
                        connection.rollback()      
                  raise

      def get_match_history_player(self, player: dict, start: int=0,count : int=20) -> list:
            """Description:
            This function utilizes the library request to send an HTTP GET request to a specified API endpoint containing a User's match history using the requests library and returns the response in JSON format.
            It combines various strings componets of RiotsAPI html such as the summoner and query string determined by RIOT with a user's id and YOURAPIKEY
            Parameters:
            - player : dictionary containing a user's informatoin
            - start : int default value = 0
            A match history is based on most recent games played in descending order. Start indicates how many games after a player's most recent game for the beginning of the list
            - count : int default value = 20 Count indicates when to stop adding matches to the history. Creates the size of the list
            Returns: A list containing match's ids
            """
            time.sleep(1.5)
            range = f"/ids?start={start}&count={count}"
            http = (match + match_history + player['puuid'] + range + find + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')
   
      def get_match_history_puuid(self, puuid: str, start: int=0, count: int=20) -> list:
            """Description:
            This function is similar to get_match_history_player except it uses a User's puuid to search for match history
            """
            time.sleep(2)    
            range = f"/ids?start={start}&count={count}" 
            http = (match + match_history + puuid + range + find + self.api_key).format(
                  regionMatch=self.region_match
            )
            try:
                  return requests.get(http).json()

            except Exception as e:
                  print(f'Could not make request {e}')

      def insert_match_history(self, connection: connect, user: dict, match_history: list) -> None:
            """Description:
            Inserts match history information into an SQL database named match_history using MySQL connector
            Parameters:
            connection: MySQL connection
            user : dictionary dictionary containing a User's information
            match_history : A list of matches from a user
            Return: None
            """
            try:
                  with connection.cursor() as cursor:
                        for item in match_history:
                              values = f"('{item}','{user['id']}','{user['accountId']}','{user['puuid']}','{user['name']}')"
                              query = f"INSERT IGNORE INTO match_history VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
                              self.insert_match_id(connection,item)
                        
            except Error as e:
                  print(f"Error: {e}")

      def insert_match_history_data(self, connection: connect, id: str, account_id: str, puuid: str, name: str , match_history: list) -> None:
            """Description:
            Similar to insert_match_history except it takes a player's info that is already parsed
            """
            try:
                  with connection.cursor() as cursor:
                        for item in match_history:
                              values = f"('{item}','{id}','{account_id}','{puuid}','{name}')"
                              query = f"INSERT IGNORE INTO match_history VALUES {values}"
                              print(query)
                              cursor.execute(query)
                              connection.commit()
                              self.insert_match_id(connection,item)
            
            except Error as e:
                  print(f"Error: {e}")

      def insert_rank_history_sql(self, connection: connect, tier: str, division: str, start: int=0, count: int=20) -> None:
            """Description:
            Retrieves and inserts all of a tier and division's players match_history and participant data into SQL database using MySQL connector to retrieve a rank's data
            Since the same players can be in different matches, the function checks if the user is already in the database.
            Uses get_summoner_info, insert_query_user,get_match_history_puuid,get_match and insert_match
            Parameters:
            connection: MySQL connection to a User's Database
            tier : str representing one of 6 tiers ("IRON","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND","MASTER","GRANDMASTER","CHALLENGER")
            division : str representing one of 4 divisions ("I","II","III","IV"), if tier is MASTER, GRANDMASTER OR CHALLENGER, DIVISION IS I
            start and count are based on get_match_history
            Return  None
            """     
            if isinstance(division,int):
                  division = self.num_roman(division)

            try:
                  with connection.cursor(buffered=True) as cursor:
                        query = f"SELECT ranked.id,ranked.account_id,ranked.puuid,ranked.name FROM ranked WHERE ranked.tier = '{tier}' AND ranked.division = '{division}'"
                        cursor.execute(query)
                        players = cursor.fetchall()
                        for item in players:
                              player_query = f"SELECT EXISTS(SELECT * FROM player WHERE player.puuid = '{item[2]}')"
                              cursor.execute(player_query)
                              exist = cursor.fetchone()[0]
                              #Using same queries to check for player in database as insert_rank. Used for the same optimization reasons
                              if exist == 0:
                                    #If user is not in database, retrieves all of a user database using the API and then retrieves master history
                                    print("player not in database")
                                    player = self.get_summoner_info_puuid(item[2])
                                    self.insert_query_user(connection,player)
                                    history = self.get_match_history_puuid(player['puuid'],start,count)
                                    self.insert_match_history(connection,player)

                              else:
                                    #If player does exist, retrieves user match history by puuid in database
                                    history = self.get_match_history_puuid(item[2],start,count)
                                    self.insert_match_history_data(connection,item[0],item[1],item[2],item[3],history) 
    
            except Exception as e:
                  print(f'Could not make request {e}')

      @staticmethod
      def get_winrate_player(connection: connect, player: dict) -> float:
            """Description:
            Retrieves a player's win rate based on which games are added into the SQL database by running query
            Parameters:
             - connection: MySQL connection to a User's Database
             - player : A dictionary representing a User's information
            Return: A decimal representing a player's win rate
            """     
            try:
                  with connection.cursor(buffered = True) as cursor:
                        #Creates query used to retrieve win rate of player in SQL database
                        wins = f"SELECT COUNT(participant.id) AS id FROM participant WHERE participant.id = '{player['id']}' AND participant.win = 1"
                        #Creates query used to retrieve total games played by player in SQL database
                        games_played = f"SELECT COUNT(participant.id) FROM participant WHERE participant.id = '{player['id']}'"
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Player: {player['name']} has no wins")
                              return total_wins
                        
                        print(f"Player: {player['name']} has a win rate of {total_wins*100/total_games}% in {total_games} games played ")
                        return (total_wins/total_games)
                        
            except Error as e:
                  print(f"Error has occured : {e}")

      @staticmethod
      def create_procedure_win_champion(connection: connect, champion: str) -> None:
            """Description:
            Retrieves win rate based on the champion which games are added into the SQL database by creating a precedure and then excuting
            Parameters:
             - connection: MySQL connectionto a User's Database
             - champion : int representing a Champion's ID
            Return Amount of wins a specific champion has
            """     
            try:
                  with connection.cursor() as cursor:
                        query = """
                        DROP procedure IF EXISTS `champion_winrate`;
                        DELIMITER $$
                        USE `leagueoflegends`$$
                        CREATE PROCEDURE `champion_winrate` (IN champion_name VARCHAR(20))
                        BEGIN
                        SELECT COUNT(part.win) FROM participant as part WHERE part.win = 1 AND part.champion_name = champion_name;
                        END$$
                        DELIMITER ;
                        """
                        cursor.execute(query)
                        win = f"CALL champion_winrate('{champion}')"
                        cursor.execute(win)
                        wins = cursor.fetchone()
                        print(wins)
                        return (wins)

            except Error as e:
                  print(f"Error has occured: {e}")

      @staticmethod
      def get_winrate_champion(connection: connect, champion: str) -> float:
            """Description:
            Retrieves a champion's win rate based on which games are added into the SQL database by running query
            Parameters:
             - connection: MySQL connection
             - champion: str representing a champion's name
            Return: decimal champion winrate
            """     
            try:
                  with connection.cursor(buffered = True) as cursor:
                        #Creates query used to retrieve win rate of champion in SQL database
                        wins = f"SELECT COUNT(participant.win) FROM participant WHERE participant.champion_name = '{champion}' AND participant.win = 1"
                        games_played = f"SELECT COUNT(participant.champion_name) FROM participant WHERE participant.champion_name = '{champion}'"
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Champion: {champion} has no wins")
                              return total_wins
                        
                        print(f"Champion: {champion} has a win rate of {total_wins*100/total_games} % in {total_games} games played")
                        return (total_wins/total_games)
  
            except Error as e:
                  print(f"Error has occured : {e}")
            
      @staticmethod

      def get_best_champions(connection: connect) -> list:
            """Description:
            Retrieves a the top 5 champions basedon which games are added into the SQL database by running query
            Parameters:
             - connection: MySQL connection
            Return: A list of top 5 champions in descending order
            """     
            try:
                  with connection.cursor(buffered = True) as cursor:
                        #Creates query used to retrieve win rate of champion in SQL database
                        all_champions = "SELECT champion_name FROM champion"
                        cursor.execute(all_champions)
                        champions = cursor.fetchall()
                        champ_winrate = {}
                        winrate = []
                        for champ in champions:
                              wins = f"SELECT COUNT(participant.win) FROM participant WHERE participant.champion_name = '{champ}' AND participant.win = 1"
                              games_played = f"SELECT COUNT(participant.champion_name) FROM participant WHERE participant.champion_name = '{champ}'"
                              cursor.execute(wins)
                              total_wins = cursor.fetchone()[0]
                              cursor.execute(games_played)
                              total_games =cursor.fetchone()[0]
                              champ_winrate[champ] = total_wins/total_games
                              winrate.append(total_wins/total_games)
                        
                        winrate = sorted(winrate)
                        k = len(winrate)
                 
                        return (total_wins/total_games)
  
            except Error as e:
                  print(f"Error has occured : {e}")


      def get_winrate_player_champion(connection, player: dict, champion: str) -> float:
            """Description:
            Retrieves a player's win rate based on which games are added into the SQL database and by champion name
            Parameters:
             - connection: MySQL connection
            A connection to a User's Database
             - player : dictionary having User's information
             - champion : str champion name
            Return : win rate decimal
            """     
            try:
                  with connection.cursor(buffered = True) as cursor:
                        #Creates query used to retrieve win rate of champion with a player in SQL database
                        wins = f"SELECT COUNT(participant.id) AS id FROM participant WHERE participant.id = '{player['id']}' AND participant.win = 1 AND participant.champion_name = '{champion}'" 
                        games_played = f"SELECT COUNT(participant.id) FROM participant WHERE participant.id = '{player['id']}' participant.champion_name = '{champion}'"
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Player: {player['name']} has no wins")
                              return total_wins
                        
                        print(f"Player: {player['name']} has a win rate of {total_wins*100/total_games}% in {total_games} games played ")
                        return (total_wins/total_games)
                        
            except Error as e:
                  print(f"Error has occured : {e}")
      


      @staticmethod
      def get_winrate_champion_rank(connection, champion: connect, rank: str, division:str) -> float:
            """Description:
            Retrieves a player's win rate based on which games are added into the SQL database and by champion name
            Parameters:
            connection: MySQL connection to a User's Database
            tier : str representing one of 6 tiers ("IRON","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND","MASTER","GRANDMASTER","CHALLENGER")
            division : str representing one of 4 divisions ("I","II","III","IV"), if tier is MASTER, GRANDMASTER OR CHALLENGER, DIVISION IS I
            champion : str champion name
            Return : win rate decimal
            """
            try:
                  with connection.cursor(buffered = True) as cursor:
                        #Creates query used to retrieve win rate of champion with a rankin SQL database
                        wins = f"""
                        SELECT COUNT(participant.win)
                        FROM participant
                        INNER JOIN ranked 
                        ON participant.id = ranked.id
                        WHERE participant.id = ranked.id AND participant.champion_name = '{champion}' AND ranked.tier = '{rank}' AND ranked.division = '{division}' AND participant.win = 1
                        """
                        #Creates query used to retrieve total games of champion with a rank in SQL database
                        games_played = f"""
                        
                        SELECT COUNT(participant.win)
                        FROM participant
                        INNER JOIN ranked 
                        ON participant.id = ranked.id
                        WHERE participant.id = ranked.id AND participant.champion_name = '{champion}' AND ranked.tier = '{rank}' AND ranked.division = '{division}'
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games =cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Champion: {champion} has no wins")
                              return total_wins
                        
                        print(f"Champion: {champion} has a win rate of {total_wins*100/total_games}% in {total_games} games played at the rank {rank} {division}")
                        return (total_wins/total_games)
                        

            except Error as e:
                  print(f"Error has occured : {e}")


      @staticmethod
      def get_winrate_item(connection: connect, item: str) -> float:
            """Description:
            Retrieves a items's win rate based on which games are added into the SQL database by running query
            Parameters:
             - connection: MySQL connection to a User's Database
             - item: str representing an items name
            Return: win rate decimal
            """
            try:
                  with connection.cursor(buffered = True) as cursor:
                        if isinstance(item,str):
                              #Creates query used to retrieve win rate of item in SQL database
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name =  item
                              item_id = cursor.fetchone()[0]
                        elif isinstance(item,int):
                              query = f"SELECT item_name FROM items WHERE items.item_id = {item}"
                              cursor.execute(query)
                              item_name =  cursor.fetchone()[0]
                              item_id = item

                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.win = 1
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id})
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant as p
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()[0]
                        cursor.execute(times_played)
                        total_participants = cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Item:{item_name} has no wins")
                              return total_wins
            
                        print(f"Item:{item_name} has a win rate of {total_wins*100/total_games_item}% in {total_games_item} games played with a buy rate of {total_games_item*100/total_participants}%")
                        return (total_wins/total_games_item)
                        
            except Error as e:
                  print(f"Error has occured : {e}")

      @staticmethod
      def get_winrate_item_rank(connection: connect, item: str, rank: str, division: str) -> float:
            """Description:
            Retrieves a items's win rate based on which games are added into the SQL database by running query and by the rank
            Parameters:
            connection: MySQL connection to a User's Database
            item: str representing an items name
            tier : str representing one of 6 tiers ("IRON","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND","MASTER","GRANDMASTER","CHALLENGER")
            division : str representing one of 4 divisions ("I","II","III","IV"), if tier is MASTER, GRANDMASTER OR CHALLENGER, DIVISION IS I
            Return: win rate decimal
            """
            try:
                  with connection.cursor(buffered = True) as cursor:
                        if isinstance(item,str):
                              #Creates query used to retrieve win rate of item in a rank in SQL database
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name =  item
                              item_id = cursor.fetchone()[0]
                        elif isinstance(item,int):
                              query = f"SELECT item_name FROM items WHERE items.item_id = {item}"
                              cursor.execute(query)
                              item_name =  cursor.fetchone()[0]
                              item_id = item
                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.win = 1 AND ranked.tier = '{rank}' AND ranked.division = '{division}'
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND ranked.tier = '{rank}' AND ranked.division = '{division}'
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE ranked.tier = '{rank}' AND ranked.division = '{division}' 
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()[0]
                        cursor.execute(times_played)
                        total_games = cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Item:{item_name} has no wins")
                              return total_wins
                        print(f"Item:{item_name} has a win rate of {total_wins*100/total_games_item}% in {total_games_item} games played with a buy rate of {total_games_item*100/total_games}% in rank {rank} {division}" )
                        return (total_wins/total_games_item)
                        
            except Error as e:
                  print(f"Error has occured : {e}")

      @staticmethod
      def get_winrate_champion_item(connection: connect, champion: str, item: str) -> float:
            """Description:
            Retrieves a items's win rate based on which games are added into the SQL database by running query and by champion name
            Parameters:
            connection: MySQL connection to a User's Database
            item: str representing an items name
            champion : str representing a champion's name
            Return: win rate decimal
            """
            try:
                  with connection.cursor(buffered = True) as cursor:
                        if isinstance(item,str):
                              #Creates query used to retrieve win rate of champion with item in SQL database
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name =  item
                              item_id = cursor.fetchone()[0]
                        elif isinstance(item,int):
                              query = f"SELECT item_name FROM items WHERE items.item_id = {item}"
                              cursor.execute(query)
                              item_name =  cursor.fetchone()[0]
                              item_id = item
                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.champion_name = '{champion}' AND p.win = 1
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.champion_name = '{champion}'
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        WHERE p.champion_name = '{champion}'
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()[0]
                        cursor.execute(times_played)
                        total_games = cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Item:{item_name} and champion: {champion} has no wins")
                              return total_wins
                        
                        print(f"Item:{item_name} has a win rate of {total_wins*100/total_games_item}% in {total_games_item} games played with a buy rate of {total_games_item*100/total_games}% on the champion {champion}" )
                        return total_games_item,(total_wins/total_games_item)
                        
            except Error as e:
                  print(f"Error has occured : {e}")

      @staticmethod
      def get_winrate_champion_item_rank(connection: connect, champion: str, item: str, rank: str, division: str) -> None:
            """Description:
            Retrieves a champion, items and rank's win rate based on which games are added into the SQL database by running query a
            Parameters:
            connection: MySQL connection to a User's Database
            champion : str representing a champion's name
            item: str representing an items name
            tier : str representing one of 6 tiers ("IRON","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND","MASTER","GRANDMASTER","CHALLENGER")
            division : str representing one of 4 divisions ("I","II","III","IV"), if tier is MASTER, GRANDMASTER OR CHALLENGER, DIVISION IS I
            Return: win rate decimal
            """
            try:
                  with connection.cursor(buffered = True) as cursor:
                        if isinstance(item,str):
                              #Creates query used to retrieve win rate of champion with item in a certain rank in SQL database
                              query = f"SELECT item_id FROM items WHERE items.item_name = '{item}'"
                              print(query)
                              cursor.execute(query)
                              item_name =  item
                              item_id = cursor.fetchone()[0]
                        elif isinstance(item,int):
                              query = f"SELECT item_name FROM items WHERE items.item_id = {item}"
                              cursor.execute(query)
                              item_name =  cursor.fetchone()[0]
                              item_id = item
                        wins = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND p.win = 1 AND ranked.tier = '{rank}' AND ranked.division = '{division}' AND p.champion_name = '{champion}'
                        """
                        games_played = f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE (p.item0 = {item_id} OR p.item1 = {item_id} OR p.item2 = {item_id} OR p.item3 = {item_id} OR p.item4 = {item_id} OR p.item5 = {item_id} OR p.item6 = {item_id}) AND ranked.tier = '{rank}' AND ranked.division = '{division}' AND p.champion_name = '{champion}'
                        """
                        times_played =  f"""
                        SELECT COUNT(p.win)
                        FROM participant AS p
                        INNER JOIN ranked
                        ON p.id = ranked.id
                        WHERE ranked.tier = '{rank}' AND ranked.division = '{division}' AND p.champion_name = '{champion}'
                        """
                        cursor.execute(wins)
                        total_wins = cursor.fetchone()[0]
                        cursor.execute(games_played)
                        total_games_item =cursor.fetchone()[0]
                        cursor.execute(times_played)
                        total_games = cursor.fetchone()[0]
                        if total_wins == 0:
                              print(f"Item:{item_name} has no wins")
                              return total_wins
                        
                        print(f"Item:{item_name} has a win rate of {total_wins*100/total_games_item}% in {total_games_item} games played with a buy rate of {total_games_item*100/total_games}% in rank {rank} {division}" )
                        return (total_wins/total_games_item)
                        
            except Error as e:
                  print(f"Error has occured : {e}")        

      
def analyze_champion_winrate(connection: connect, query: str):
      """
      Retrieve data from a MySQL database, convert it to a Pandas dataframe, and plots champion win rate using Plotly. The query determines what the win rate is based off.
      Example
      que = "SELECT * FROM participant INNER JOIN ranked ON participant.id = ranked.id" This queue only selects participants with a certain rank
      que2 = "SELECT * FROM participant"  This queue selects all participants and anaylzes every user
      Parameter 
      query (str): The SQL query to execute to retrieve data from the database.
      Returns:
        fig: A Plotly scatter plot with labeled axes from champion.
      Raises:
         mysql.connector.Error: If there is an error connecting to or querying the database.
    """
      try:
            with connection.cursor(buffered=True) as cursor:
                        print(f"Excuting: {query}")
                        cursor.execute(query)
                        column_names = [i[0] for i in cursor.description] 
                        df = pd.DataFrame(cursor.fetchall(), columns = column_names)
                        df_winrate = df.groupby(['champion_name']).sum('win').sort_values('champion_name')
                        df_winrate['total_games'] = df.groupby(['champion_name']).count().sort_values('champion_name')['win']
                        df_winrate['winrate'] = df_winrate['win']/df_winrate['total_games']
                        df_winrate['champion_name'] = df_winrate.index.tolist()
                        fig = px.scatter(df_winrate, x="champion_name", y="winrate", text="champion_name", log_x=False, size_max= 1)
                        fig.update_traces(textposition='top center')
                        fig.update_layout(title_text='Win rate by champion', title_x=0.5)
                        fig.show()
                        return fig    

      except Exception as e:
            print(f"Error: {e}")

def analyze_champion_playrate(connection: connect, query: str):
      """
      Retrieve data from a MySQL database, convert it to a Pandas dataframe, and plots champion play rate using Plotly. The query determines what the play rate is based off
      Parameter 
      query (str): The SQL query to execute to retrieve data from the database.
      Returns:
        fig: A Plotly scatter plot with labeled axes from champion.
      Raises:
         mysql.connector.Error: If there is an error connecting to or querying the database.
    """
      try:
            with connection.cursor(buffered=True) as cursor:
                  print(f"Excuting: {query}")
                  cursor.execute(query)
                  column_names = [i[0] for i in cursor.description] 
                  df = pd.DataFrame(cursor.fetchall(), columns = column_names)
                  df_playrate = df.groupby(['champion_name']).sum().sort_values('champion_name')
                  df_playrate['times_played'] = df['champion_name'].value_counts()
                  amount_matches = len(df['match_id'].unique())
                  df_playrate['play_rate'] = df_playrate['times_played']/amount_matches
                  df_playrate['champion_name'] = df_playrate.index.tolist()
                  fig = px.scatter(df_playrate, x="champion_name", y="play_rate", text="champion_name", log_x=False, size_max= 1)
                  fig.update_traces(textposition='top center')
                  fig.update_layout(title_text='Play rate by champion', title_x=0.5)
                  fig.show()
                  return fig    

      except Exception as e:
            print(f"Error: {e}")


def analyze_item_purchase_rate(connection: connect, query: str):
      """
      Retrieve data from a MySQL database, convert it to a Pandas dataframe, and plots champion win rate using Plotly. The query determines what the win rate is based off
      Parameter 
      query (str): The SQL query to execute to retrieve data from the database.
      Returns:
        fig: A Plotly scatter plot with labeled axes from champion.
      Raises:
         mysql.connector.Error: If there is an error connecting to or querying the database.
    """
      try:
            with connection.cursor(buffered=True) as cursor:
                  print(f"Excuting: {query}")
                  cursor.execute(query)
                  column_names = [i[0] for i in cursor.description] 
                  df = pd.DataFrame(cursor.fetchall(), columns = column_names)
                  item_query = "SELECT * FROM items"
                  cursor.execute(item_query)
                  column_names = [i[0] for i in cursor.description] 
                  df_item = pd.DataFrame(cursor.fetchall(), columns = column_names)
                  df_item['count'] = 0
                  items = df_item[['item_name','count']].to_numpy()
                  item_bought = df[['item0_name','item1_name','item2_name','item3_name','item4_name','item5_name','item6_name']].to_numpy()
                  for i in range(len(item_bought[0])):    
                        for j in range(len(item_bought)):
                              item = item_bought[j][i]
                              if item != "No item":
                                    item_index = np.where(items == item)
                                    items[(item_index[0][0])][1] += 1
                  df_item_count = pd.DataFrame(items, columns = ['item_name','amount_bought']) 
                  amount_matches = len(df['match_id'].unique())
                  df_item_count['purchase_rate'] = df_item_count['amount_bought']/amount_matches
                  fig = px.scatter(df_item_count, x="item_name", y="purchase_rate", text="item_name", log_x=False, size_max= 1)
                  fig.update_traces(textposition='top center')
                  fig.update_layout(title_text='Purchase rate', title_x=0.5)
                  fig.show()
                  return fig

      except Exception as e:
            print(f"Error: {e}")
            
def sql_csv(connection: connect, query : str, name_csv: str, index: bool=False):
      """
    Execute a SQL query on a MySQL database, convert the result to a Pandas dataframe,
    and save it as a CSV file.

      Parameter
      query (str): The SQL query to execute.
      filename (str): The name of the CSV file to save the data to.
      index (bool): Determines if a csv file with have index or not, default value is false
      
      Raises:
        mysql.connector.Error: If there is an error connecting to or querying the database.
        OSError: If there is an error saving the CSV file.

      
      """
      try:
            with connection.cursor(buffered=True) as cursor:
                  print(f"Excuting: {query}")
                  cursor.execute(query)
                  #Gets the columns names
                  column_names = [i[0] for i in cursor.description]
                  #Creates dataframe with all data in SQL date with the columns names 
                  df = pd.DataFrame(cursor.fetchall(), columns = column_names)                  
                            
      except Exception as e:
            print(f"Error: {e}")

      try:
            df.to_csv(f"{name_csv}.csv",index=index)

      except OSError as err:
        raise err

que = "SELECT * FROM participant INNER JOIN ranked ON participant.id = ranked.id"
que2 = "SELECT * FROM participant"
que3 = "SELECT * FROM items"
naServer = RiotAPI(api_key,"americas","na1")


"""
champ = naServer.get_champion()
item = naServer.get_items()
challenger = naServer.get_challenger()
D1 = naServer.get_rank("DIAMOND","I")
naServer.insert_all_rank(connection,D1)
"""
challenger = naServer.get_challenger()


try:
      with connect(
            host= my_host,
            user= my_username,
            password= my_password,
            database = my_database,
      ) as connection:
            print(f"Connection {connection}")
            """
            naServer.insert_champions(connection,champ)
            naServer.insert_items(connection,item)
            naServer.insert_rank_history_sql(connection,"CHALLENGER","I",0,10)
            """
            naServer.insert_high_rank(connection,challenger)
            naServer.insert_rank_history_sql(connection,"CHALLENGER","I",0,10)
            
            
except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Either your user name or password is incorrect")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            naServer.insert_rank_history_sql(connection,"CHALLENGER","I")
            sql_csv(connection,que,"challenger")

        else:
            print(e)
