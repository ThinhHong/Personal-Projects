#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve


# ### League of Legends is a multiplayer online battle arena game that involves two teams of five players each competing against each other to destroy the enemy's base while defending their own.

# In[33]:


df = pd.read_csv("C:/Users/Thinh/Documents/Github/Personal-Projects/League/all_participants.csv")


# # Classification 

# In[34]:


df.head()


# ### Here are some of the factors that can lead to a win in League of Legends:
# ### Champion selection: Picking the right champion for your role and for the team composition is crucial. Each champion has unique abilities and strengths, play and win rate and picking the right combination of champions can give your team an advantage in team fights.
# 
# ### Gold management: There are several ways  to earn gold, which can be used to purchase items and boost your champion's abilities. God management can give your team an economic advantage, allowing you to buy better items and gain more power.
# 
# ### Objectives: Destroying turrets, securing dragon and Baron kills, and pushing lanes are all crucial objectives in League of Legends. These objectives provide strategic advantages, such as extra gold and experience, which can help your team gain a lead and ultimately win the game.
# 
# ### Kills: Killing an enemy champion can lead to a huge gold and exp boost. When a champion is dead, they remain unable to play the game for some time. Making the player lose exp,gold and the team loses strength.
# 
# ### Farming: Farming refers to killing minions and monsters to earn gold and exp
# 
# ### The goal of the dataset analysis is predict whether or not a participant would win based on the independent variables

# ## Dataset analysis 

# In[35]:


df.shape


# In[36]:


df.info()


# ### There are no null values in this dataframe. 20150/20150 rows are non-null for every column except team position. In the all_participant data frame, there is a variety of columns having types of either integer64 or object(strings).

# # Data cleanup
# ### As the participant data is based on the data in the SQL server, there is a chance for NAN values to be present
# 

# In[37]:


df_no_nan = df[df.isna().any(axis=1)]
df_no_nan.head()


# In[19]:


df_no_nan = df_no_nan.dropna(how='all')


# ### Adding side column indicating whether a participant was on the red side or the blue side. All participants on the same side and same match are on the same team.

# In[38]:


df.rename(columns={'participate_id' : 'participant_id'},inplace=True )
df['side'] = pd.Series('blue', index=df.index).mask(df['participant_id']>5,'red')
df


# ### Adding champion winrate column

# In[39]:


df_winrate = df.groupby(['champion_name']).sum().sort_values('champion_name')
df_winrate['total_games'] = df.groupby(['champion_name']).count().sort_values('champion_name')['win']
df_winrate['champion_winrate'] = df_winrate['win']/df_winrate['total_games']
df_winrate['champion_name'] = df_winrate.index.tolist()
df_winrate.reset_index(drop=True,inplace=True)
df = df.merge(df_winrate[['champion_name','champion_winrate']], on='champion_name').sort_values(['match_id','participant_id'])
df


# ### Adding champion playrate column

# In[41]:


df_playrate = df.groupby(['champion_name']).sum().sort_values('champion_name')
df_playrate['times_played'] = df['champion_name'].value_counts()
amount_matches = len(df['match_id'].unique())
df_playrate['champion_playrate'] = df_playrate['times_played']/amount_matches
df_playrate['champion_name'] = df_playrate.index.tolist()
df_playrate.reset_index(drop=True,inplace=True)
df = df.merge(df_playrate[['champion_name','champion_playrate']], on='champion_name').sort_values(['match_id','participant_id'])
df


# # Visualization

# In[84]:


df_winrate = df_winrate.sort_values('champion_name')
df_playrate = df_playrate.sort_values('champion_name')
plt.scatter(df_playrate['champion_playrate'],df_winrate['champion_winrate'],color = 'purple',marker = 'o')
plt.title('Playrate vs Winrate',fontsize=13)
plt.xlabel('playrate of champion',fontsize=13)
plt.ylabel('winrate of champion',fontsize=13)
plt.show()


# In[97]:


fig, ax = plt.subplots(figsize = (6,4))
ax.hist(df['champion_winrate'], bins = 15)
ax.set_xlabel("Champion winrate")
ax.set_title("Winrate of champions based on SQL query")
plt.show()


# In[105]:


fig, ax = plt.subplots(figsize = (6,4))
winrate = df['champion_winrate']
winrate.plot(kind = "hist", range = (0.3,0.7), density = True, bins = 20)
winrate.plot(kind = "kde")
ax.set_xlabel("Champion winrate")
ax.set_ylim(0,11)
ax.set_title("Winrate of champions based on SQL query")
ax.set_yticks([])
ax.set_ylabel("")
ax.tick_params(left = False, bottom = False)
for ax, spine in ax.spines.items():
    spine.set_visible(False)

plt.show()


# In[102]:


fig, ax = plt.subplots(figsize = (6,4))
winrate = df['champion_winrate']
x.min()


# In[ ]:




