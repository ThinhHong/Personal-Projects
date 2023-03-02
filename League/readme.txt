Riot API Data Analysis Project
This project is a data analysis tool that uses the Riot API to gather data on League of Legends matches and perform statistical analysis on that data. The project consists of several components:

API requests to gather data from the Riot API
Uploading data to a SQL database
Data visualization and analysis using Plotly and Pandas
Getting Started
To use this project, you'll need to sign up for your own personal API key from the Riot API website. This key will allow you to make requests to the API and gather data on League of Legends matches. 
Once you have your key, you'll need to add it to the config.py file and run it, as described below.

Using the API
To make a request to the Riot API, you'll need to use the requests library in Python. The RiotAPI.py file contains several functions that make requests to the API 
and return the resulting data as a JSON object that is converted to a dictionary.
All request are put on a 1.5 sleep timer in order to comply with Riot's API rules indicating that RATE LIMITS
20 requests every 1 seconds(s)
100 requests every 2 minutes(s)
Note that rate limits are enforced per routing value (e.g., na1, euw1, americas)
Rate limits can be improved by obtaining a better production key from RIOT.


Uploading Data to SQL
Once you've gathered data from the Riot API, you can upload that data to a SQL database using the mysql.connector library in Python. 
The RiotAPI.py file contains several functions that handle database connections, SQL queries, and data insertion.

Data Visualization and Analysis
Finally, you can use the RiotAPI.py file to generate plots and perform statistical analysis on the data. 
This file uses the pandas and plotly libraries to manipulate and visualize the data.

Configuration
All table creations and alters in the SQL file need to be ran first to create the needed tables.
Before running the project, you'll need to configure the config.py file with your Riot API key and database credentials. 
To do this, copy the config.py file  and fill in the appropriate values. You'll need to provide the following information:

Your MySQL host name
Your Riot API key, API key is personalized and should not be shared online
The name of your MySQL database
The username and password for your MySQL database

Required Steps
Functions get_champion, get_items, insert_champions_,insert_items should be called first.
In order to use insert_rank_sql, functions get_rank and insert_rank with the same parameters need to be called.
insert_match_history requires a user to be already inserted using insert_query_user.
The get functions are used to retrieve the JSON data from Riot and 

Conclusion
That's it! With your API key and database credentials configured, you should be able to run the project and start gathering data on League of Legends matches. 
From there, you can use the tools in the RiotAPI.py file to visualize and analyze the data, and gain insights into the world of League of Legends.
Examples include retrieving all challenger players and another rank and comparing the win rates between them based on other factors such as items, masteries,champions and play rate.

League of Legends (LoL) is a multiplayer online battle arena (MOBA) video game developed and published by Riot Games. 
It is a team-based game where two teams of five players each compete against each other on a map called the "Summoner's Rift". The game has a large player base and is played competitively in various leagues and tournaments around the world.
In League of Legends, players take on the role of a "champion", each with unique abilities and playstyles. 
Players start the game at level 1 and earn experience points and gold by killing minions, neutral monsters, and other player's champions. As they level up, they gain access to more powerful abilities and items, allowing them to deal more damage.

Overall, League of Legends is a fast-paced and complex game that requires strategy, teamwork, and skill to master. 
It has a large and active player base, and is played competitively at both the amateur and professional levels.
Players can be of many different tiers, divisions and points. They can earn mastery on the champion played depending on how well they do.