from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.graph_objs import *

df = pd.read_csv("all_participants.csv")
df_champion = pd.read_csv("champions.csv")
df_champion['times_played'] = 0
df_champion['times_won'] = 0
df['side'] = pd.Series('blue', index=df.index).mask(df['participant_id']>5,'red')
#champion names in the particpant table and champion csv file are lowercased to ensure names are equivalent
df_champion['champion_name'] = df_champion['champion_name'].apply(str.lower)
df['champion_name'] = df['champion_name'].apply(str.lower)

#champion names in the particpant table and champion csv file are removed of whitespace to ensure names are equivalent
df_champion['champion_name'] = df_champion['champion_name'].apply(str.strip)
df['champion_name'] = df['champion_name'].apply(str.strip)

df_winrate = df.groupby(['champion_name']).sum().sort_values('champion_name')
df_winrate['total_games'] = df.groupby(['champion_name']).count().sort_values('champion_name')['win']
df_winrate['champion_winrate'] = df_winrate['win']/df_winrate['total_games']
df_winrate['champion_name'] = df_winrate.index.tolist()
df_winrate.reset_index(drop=True,inplace=True)
df = df.merge(df_winrate[['champion_name','champion_winrate']], on='champion_name').sort_values(['match_id','participant_id'])
df_champion= df_champion.merge(df_winrate[['champion_name','champion_winrate']], on='champion_name')

df_playrate = df.groupby(['champion_name']).sum().sort_values('champion_name')
df_playrate['times_played'] = df['champion_name'].value_counts()
#The total amount of matches is the amount of unique match ids
amount_matches = len(df['match_id'].unique())
df_playrate['champion_playrate'] = df_playrate['times_played']/amount_matches
df_playrate['champion_name'] = df_playrate.index.tolist()
df_playrate.reset_index(drop=True,inplace=True)
df = df.merge(df_playrate[['champion_name','champion_playrate']], on='champion_name').sort_values(['match_id','participant_id'])

df_champion = df_champion.merge(df_playrate[['champion_name','champion_playrate']], on='champion_name').sort_values('champion_name')
champion_list = df_champion['champion_name'].unique().tolist()

df_item = pd.read_csv("items.csv")
#Creates count for every item in item.csv and sets to 0
df_item['count'] = 0
#converts items df to numpy
items = df_item[['item_name','count','item_id']].to_numpy()
#Selects all columns an item appears in
item_bought = df[['item0_name','item1_name','item2_name','item3_name','item4_name','item5_name','item6_name']].to_numpy()
#iterates through length of all item_bought bought by a participant
for i in range(len(item_bought[0])):
    #iterates through length of all item_bought to get every participates purchased items
    for j in range(len(item_bought)):
        #gets item name that a participant bought
        item = item_bought[j][i]
        if item != "No item":
            #finds the index in items array that a participant bought
            item_index = np.where(items == item)
            #Adds 1 to counter 
            items[(item_index[0][0])][1] += 1
df_item_count = pd.DataFrame(items, columns = ['item_name','amount_bought','item_id']) 
df_item_count['purchase_rate'] = df_item_count['amount_bought']/amount_matches
df_item_count.sort_values('purchase_rate',ascending = False)
item_list = df_item_count['item_name'].unique().tolist()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

fig_item = px.scatter(df_item_count, x="item_name", y="purchase_rate", text="item_name", log_x=False, size_max= 1)
fig_item.update_traces(textposition='top center')
fig_item.update_layout(title_text='Purchase rate', title_x=0.5)



introduction = """
    Welcome to my league of legends dash application. Here you will be able to find information such as 
    your favorite champion's win rate or playrate. As well as the purchase rate of items
"""


app = Dash(__name__, external_stylesheets=external_stylesheets, title='League of Legends Analytics')

app.layout = html.Div(style={'backgroundColor':'lightblue'},children=[
        html.H1(className='middle', children='League of legends dash application',
                    style={'textAllign': 'center', 'color': 'gold', 'fontSize': 40, 'backgroundColor':'darkblue'}),
        html.Div(style={'backgroundColor':'blue'},children=[
            dcc.Markdown(children=introduction,style={'backgroundColor':'lightblue'})
        ]),
        html.Div(className='row', children=[
          'Champion_name',
        dcc.Dropdown(options=champion_list, id='champion_name', value='aatrox',style={'backgroundColor':'lightblue'}),
        ]),
        html.Br(),
        html.Div(className='row', children=[
            html.Img(id='champion_image', height= 80,alt= "Champion icon does not exist"),
            html.Div(id='champion_stats')
        ]),
        html.Div(className='champ', children=[
            "Champion History",
            dash_table.DataTable(id='champion_history', page_size=11, style_table={'overflowX':'auto', 'backgroundColor':'lightblue'})
        ]),

        html.Div(className='row', children=[
            "Item",
            dcc.Dropdown(options=item_list, id='item_name', value="Doran's Blade",style={'backgroundColor':'lightblue'})
        ]),
        html.Div(className='row', children=[
            html.Img(id='item_image', height=80, alt="Item icon does not exist"),
            html.Div(id='item_stats')
        ]),
        html.Div(className='df', children=[html.Div([
        "match id: ",
        dcc.Input(id='match_control', value="NA1_4550653187", type='text',style={'backgroundColor':'lightblue'}),
        dash_table.DataTable( id='match_output', page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='row',children=[
            dcc.RadioItems(options=['champion_winrate','champion_playrate'],
                           value='champion_winrate',
                           inline=True,
                           id = 'champion_control')
        ]),
        html.Div(className='row',children=[
                dcc.Graph(figure={}, id='champion_graph_output')
            ]),
        html.Div(className='row',children=[
                dcc.Graph(figure=fig_item)
            ])
        ])

    ])

@app.callback(
    Output(component_id='champion_image',component_property='src'),
    Output(component_id='champion_stats',component_property='children'),
    Input(component_id='champion_name', component_property='value')
)
def update_champion(champion_name: str) -> str:
    #Searches for champion
    champion = df_champion[df_champion['champion_name'] == champion_name]
    #gets winrate
    winrate = round(champion['champion_winrate'].to_numpy()[0],2)
    #gets playrate
    playrate = round(champion['champion_playrate'].to_numpy()[0],2)
    output = f"Champion: {champion_name} has a winrate of {winrate}% and a playrate of {playrate}% in {amount_matches} matches"
    return f'http://ddragon.leagueoflegends.com/cdn/13.7.1/img/champion/{champion_name.capitalize()}.png', output

@app.callback(
    Output(component_id='item_image',component_property='src'),
    Output(component_id='item_stats',component_property='children'),
    Input(component_id='item_name', component_property='value')
)
def update_item(item_name: str) -> str:
    #Searches for item
    item = df_item_count[df_item_count['item_name'] == item_name]
    #Gets purchase rate
    playrate = round(item['purchase_rate'].to_numpy()[0],2)
    item_id =  item['item_id'].to_numpy()[0]
    output = f"Champion: {item_name} has a purchase rate of {playrate}% in {amount_matches} matches"
    return f'http://ddragon.leagueoflegends.com/cdn/13.7.1/img/item/{item_id}.png', output


@callback(
    Output(component_id='champion_graph_output', component_property='figure'),
    Input(component_id='champion_control', component_property='value'),
)
def update_gph(col: str):
    #Creates a graph depending on the column value
    fig = px.scatter(df_champion, x="champion_name", y=col, text="champion_name", log_x=False, size_max= 1
)
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text=f"{col} by champion", title_x=0.5)
    fig.update_layout(yaxis_range=[0,1])
    return fig

@callback(
    Output(component_id='match_output', component_property='data'),
    Input(component_id='match_control', component_property='value'),
)
def update_match(match_id: str):
    #Updates
    return df[df['match_id'] == match_id].to_dict('records')

@callback(
    Output(component_id='champion_history', component_property='data'),
    Input(component_id='champion_name', component_property='value'),
)
def update_champ_history(champion_name: str):
    #Updates matches of champion
    return df[df['champion_name'] == champion_name].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_hot_reload=True)