Riot API Data Analysis Project

League of Legends (LoL) is a popular multiplayer online battle arena (MOBA) video game developed and published by Riot Games. It is a free-to-play game that is 
played by millions of players worldwide. In the game, players control a "champion," a powerful character with unique abilities, and work together with their team 
to destroy the enemy team's base while defending their own.

The game is played on a map known as Summoner's Rift, which features three lanes that connect the two bases. Players must navigate these lanes, battling enemy 
champions and computer-controlled minions, in order to destroy the enemy team's towers and ultimately their Nexus.

Each champion has a set of abilities that can be leveled up as the game progresses, as well as a unique playstyle and strengths and weaknesses. Players can 
choose from a wide variety of champions, each with their own distinct personality and backstory.

League of Legends is also known for its competitive scene, with professional players and teams competing in international tournaments for large cash prizes. 
The game is constantly updated with new champions, gameplay mechanics, and features to keep players engaged and the community active

Dependencies:

scikit-learn
xgboost
matplotlab
pandas
plotly
seaborn
Install missing dependencies with pip install or anaconda

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
This particular dataset retrieves all 200 of the current challenger players on March 15,2023. It retrieves 5 of their previous matches and their game detailes for a total of 1000 matches
and 10000 participants. 
Finally, you can use the RiotAPI.py file to generate plots and perform statistical analysis on the data. 
This file uses the pandas and plotly libraries to manipulate and visualize the data.
The csv file all_paricipants and items was analyzed using jupyter notebook. The ipynb file named
data analysis solves questions such as which champions have the highest win rate,
most popular items and champion. Assess the normality of champion win rate depending on
play rate of champion.

Predicting Winner of match
Several machine learning algorithms are implemented to predict the winner of the match based on overall team data found at the end of a match. Uses mlp, logistic regression and 
xgboost and analyzed using f1 scores and classification reports

Dashboard

Dashboard reads a csv named all_participants. In order to retrieve data, run function in Riot API sql_csv. In Dashboard app, change read file to view any data you have collected and wish to view.
A dashboard was implemented using plotly to visualizing the data. It can be used to get the winrate of a champion, play rate of an item or the chances of a team winning based on end game data.
It can be used to bring the visual images of champion icons and item icons. Using  dash import Dash, html, dash_table, dcc, callback, Output, Input
It order to create the dash app, run Dashboard.py.

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
