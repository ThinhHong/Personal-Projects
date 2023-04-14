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

def get_player_winrate(connection: connect, player_name: str) -> float:
    """Description:
    Retrieves a player's win rate based on which games are added into the SQL database and by champion name
    Parameters:
        - connection: MySQL connection
    A connection to a User's Database
        - player : dictionary having User's information
        - champion : str representing a Champion's name
    Return play win rate of player
    """     
    try:
            with connection.cursor(buffered = True) as cursor:

                query = f'CALL getPlayerWinrate("{player_name}", @winrate)'
                cursor.execute(query)
                winrate = cursor.fetchone()[0]
                if winrate == None:
                        print(f"{player_name} did not play")
                        return
                print(f"{player_name} has a win rate of {winrate}")
                return winrate
            
    except Error as e:
            print(f"Error has occured : {e}")

def get_best_champions(connection: connect) -> list:
    """Description:
    Retrieves the top 5 champions winrate based on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection
    Return: A list of top 5 champions highest win rate in descending order
    """     
    try:
            with connection.cursor(buffered = True) as cursor:
                query ="""
                WITH wins AS(
                SELECT
                p.champion_name, COUNT(p.champion_name) total_win
                FROM participant AS p
                WHERE p.win = 1
                GROUP BY p.champion_name
                ),
                total AS (
                SELECT l.champion_name, total_win, COUNT(l.champion_name) total_game
                FROM participant AS l
                INNER JOIN wins AS w
                ON w.champion_name = l.champion_name
                GROUP BY w.champion_name)
                SELECT champion_name, total.total_win, total_game, total_win/total_game AS win_rate FROM total
                ORDER BY win_rate DESC
                 LIMIT 5;
               """ 
                ch = [['champion_name','total_games','rate']]
                cursor.execute(query)
                for i in range(5):
                        champ_data = []
                        data = cursor.fetchone()
                        print(f"{data[0]}, has a win rate of {data[3]} out of {data[2]} games")
                        champ_data.append(data[0])
                        champ_data.append(data[3])
                        champ_data.append(data[2])
                        ch.append(champ_data)
                return ch
    except Error as e:
            print(f"Error has occured : {e}")

def get_worst_champions(connection: connect) -> list:
    """Description:
    Retrieves the top 5 champions with the lowest winrate based  on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection
    Return: A list of top 5 champions lowest winrate in ascending order
    """      
    try:
        with connection.cursor(buffered = True) as cursor:
                query ="""
                WITH wins AS(
                SELECT
                p.champion_name, COUNT(p.champion_name) total_win
                FROM participant AS p
                WHERE p.win = 1
                GROUP BY p.champion_name
                ),
                total AS (
                SELECT l.champion_name, total_win, COUNT(l.champion_name) total_game
                FROM participant AS l
                INNER JOIN wins AS w
                ON w.champion_name = l.champion_name
                GROUP BY w.champion_name)
                SELECT champion_name, total.total_win, total_game, total_win/total_game AS win_rate FROM total
                ORDER BY win_rate ASC
                LIMIT 5;
                """ 
                cursor.execute(query)
                ch = [['champion_name','total_games','rate']]
                for i in range(5):
                      champ_data = []
                      data = cursor.fetchone()
                      print(f"{data[0]}, has a win rate of {data[3]} out of {data[2]} games")
                      champ_data.append(data[0])
                      champ_data.append(data[3])
                      champ_data.append(data[2])
                      ch.append(champ_data)
                
                return ch

    except Error as e:
            print(f"Error has occured : {e}")

def get_most_played_champions(connection: connect) -> None:
    """Description:
    Retrieves the top 5 champions playrate based on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection
    Return: A list of top 5 champions highest playrate in descending order
    """
         
    try:
            with connection.cursor(buffered = True) as cursor:
                query ="""
                SELECT champion_name, count(*) AS total_played, (SELECT COUNT(DISTINCT match_id) FROM participant) AS matches, count(*)/(SELECT COUNT(DISTINCT match_id) FROM participant) AS playrate
                FROM participant
                GROUP BY champion_name
                ORDER BY total_played DESC
                LIMIT 5;
                """
                ch = [['champion_name','total_games','rate']] 
                cursor.execute(query)
                for i in range(5):
                      data = cursor.fetchone()
                      print(f"{data[0]}, has a play rate of {data[3]} out of {data[2]} games")
                      champ_data = []
                      champ_data.append(data[0])
                      champ_data.append(data[3])
                      champ_data.append(data[2])
                      ch.append(champ_data)
                
                return ch
            
    except Error as e:
            print(f"Error has occured : {e}")

def get_least_played_champions(connection: connect) -> list:
    """Description:
    Retrieves the top 5 champions lowest playrate  based on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection
    Return: A list of top 5 champions lowest playrate in ascending order
    """     
    try:
            with connection.cursor(buffered = True) as cursor:
                query ="""
                SELECT champion_name, count(*) AS total_played, (SELECT COUNT(DISTINCT match_id) FROM participant) AS matches, count(*)/(SELECT COUNT(DISTINCT match_id) FROM participant) AS playrate
                FROM participant
                GROUP BY champion_name
                ORDER BY total_played ASC
                LIMIT 5;
                """ 
                ch = [['champion_name','total_games','rate']]
                cursor.execute(query)
                for i in range(5):
                      data = cursor.fetchone()
                      print(f"{data[0]}, has a play rate of {data[3]} out of {data[2]} games")
                      champ_data = []
                      champ_data.append(data[0])
                      champ_data.append(data[3])
                      champ_data.append(data[2])
                      ch.append(champ_data)
                
                return ch

    except Error as e:
            print(f"Error has occured : {e}")

def get_champion_winrate(connection: connect, champion_name: str) -> float:
            """Description:
            Retrieves win rate of champion based on the champion which games are added into the SQL database by creating a precedure and then excuting
            Calls procedure created in RIOTSQL
            Parameters:
             - connection: MySQL connectionto a User's Database
             - champion : str representing a Champion's name
            Return win rate of champion
            """     
            try:
                  with connection.cursor() as cursor:
                        query = f'CALL getChampionWinrate("{champion_name}", @winrate)'
                        cursor.execute(query)
                        winrate = cursor.fetchone()[0]
                        if winrate == None:
                                print("Champion was not played")
                                return
                        print(f"{champion_name} has a win rate of {winrate}" )
                        return winrate
                  
            except Error as e:
                  print(f"Error has occured: {e}")
 
def get_champion_playrate(connection: connect, champion_name: str) -> float:
            """Description:
            Retrieves play rate based of champion on the champion which games are added into the SQL database by creating a precedure and then excuting
            Parameters:
             - connection: MySQL connectionto a User's Database
             - champion : str representing a Champion's name
            Return playrate
            """     
            try:
                  with connection.cursor() as cursor:
                        query = f'CAll getChampionPlayrate("{champion_name}", @winrate)'
                        cursor.execute(query)
                        winrate = cursor.fetchone()[0]
                        if winrate == None:
                                print("Champion was not played")
                                return
                        print(f"{champion_name} has a play rate of {winrate}" )
                        return winrate
                  
            except Error as e:
                  print(f"Error has occured: {e}")                 



@staticmethod
def get_champion_rank_winrate(connection: connect, champion_name: str, tier: str, division: str) -> float:
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
def get_item_purchase_rate(connection: connect, item: str) -> float:
    """Description:
    Retrieves a items's purchase rate based on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection to a User's Database
        - item: str representing an items name
    Return: purchase rate decimal
    """
    try:
            with connection.cursor(buffered = True) as cursor:
                query = f'CAll itemPurchaseRate("{item}", @winrate)'
                cursor.execute(query)
                purchase_rate = cursor.fetchone()[0]
                print(f"Purchase rate of {item} is {purchase_rate}")
                return purchase_rate
                
    except Error as e:
            print(f"Error has occured : {e}")

def call_item_rank_purchase_rate(connection: connect, item: str, tier: str, division: str) -> float:
    """Description:
    Retrieves a items's win rate based on which games are added into the SQL database by running query
    Parameters:
        - connection: MySQL connection to a User's Database
        - item: str representing an items name
    Return: win rate decimal
    """
    try:
            with connection.cursor(buffered = True) as cursor:
                
                query = f'CAll item_purchase_rate("{item}", @winrate)'
                cursor.execute(query)
                purchase_rate = cursor.fetchone()[0]
                print(f"Purchase rate of {item} is {purchase_rate}")
                return purchase_rate
                
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
            get_item_purchase_rate(connection, "Boots")
           
except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Either your user name or password is incorrect")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
           
        else:
            print(e)