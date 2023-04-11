import sys
import configparser
import mysql.connector
from mysql.connector import connect, errorcode, Error

config = configparser.ConfigParser()
try:
    config.read('configlol.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

my_host = config['userID']['host']
my_username = config['userID']['username']
my_password = config['userID']['password']
my_database = config['userID']['database']


def get_best_champions(connection: connect) -> list:
    """Description:
    Retrieves a the top 5 champions basedon which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection
    Return: A list of top 5 champions in descending order
    """     
    try:
            with connection.cursor(buffered = True) as cursor:
                a = 2

    except Error as e:
            print(f"Error has occured : {e}")

def call_champion_winrate(connection: connect, champion_name: str) -> float:
            """Description:
            Retrieves win rate based on the champion which games are added into the SQL database by creating a precedure and then excuting
            Parameters:
             - connection: MySQL connectionto a User's Database
             - champion : int representing a Champion's ID
            Return Amount of wins a specific champion has
            """     
            try:
                  with connection.cursor() as cursor:
                        query = f'CAll GetChampionWinrate("{champion_name}", @winrate)'
                        cursor.execute(query)
                        winrate = cursor.fetchone()[0]
                        if winrate == None:
                                print("Champion was not played")
                                return
                        print(f"{champion_name} has a win rate of {winrate}" )
                        return winrate
                  
            except Error as e:
                  print(f"Error has occured: {e}")
 
def call_champion_playrate(connection: connect, champion_name: str) -> float:
            """Description:
            Retrieves win rate based on the champion which games are added into the SQL database by creating a precedure and then excuting
            Parameters:
             - connection: MySQL connectionto a User's Database
             - champion : int representing a Champion's ID
            Return Amount of wins a specific champion has
            """     
            try:
                  with connection.cursor() as cursor:
                        query = f'CAll GetChampionPlayrate("{champion_name}", @winrate)'
                        cursor.execute(query)
                        winrate = cursor.fetchone()[0]
                        if winrate == None:
                                print("Champion was not played")
                                return
                        print(f"{champion_name} has a play rate of {winrate}" )
                        return winrate
                  
            except Error as e:
                  print(f"Error has occured: {e}")                 

def call_champion_player_winrate(connection: connect, champion_name: str, player_name: str) -> float:
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

                query = f'CAll GetChampionPlayerWinrate("{champion_name}","{player_name}", @winrate)'
                cursor.execute(query)
                winrate = cursor.fetchone()[0]
                if winrate == None:
                        print(f"Champion was not played by {player_name}")
                        return
                print(f"{champion_name} has a win rate of {winrate} by {player_name}")
                return winrate
            
    except Error as e:
            print(f"Error has occured : {e}")



@staticmethod
def call_champion_rank_winrate(connection: connect, champion_name: str, tier: str, division: str) -> float:
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
                query = f'CAll GetChampionRankWinrate("{champion_name}","{tier}","{division}", @winrate)'
                cursor.execute(query)
                winrate = cursor.fetchone()[0]
                if winrate == None:
                        print(f"Champion was not played in {tier}")
                        return
                print(f"{champion_name} has a win rate of {winrate} in {tier} {division}")
                return winrate
                

    except Error as e:
            print(f"Error has occured : {e}")


@staticmethod
def call_purchaserate_item(connection: connect, item: str) -> float:
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

try:
      with connect(
            host= my_host,
            user= my_username,
            password= my_password,
            database = my_database,
      ) as connection:
            print(f"Connection {connection}")
            call_champion_playrate(connection,"LeeSin")
           
except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Either your user name or password is incorrect")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
           
        else:
            print(e)