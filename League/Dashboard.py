from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import xgboost as xgb

# Read csv file
df = pd.read_csv("all_participants.csv")
df_champion = pd.read_csv("champions.csv")
df_champion['times_played'] = 0
df_champion['times_won'] = 0
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

css = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=css)

app.layout = dmc.Container([
    dmc.Title('Leauge of legends champion and item analysis ', color='blue',size='h4'),
    dmc.RadioGroup( 
                [dmc.Radio(i, value=i) for i in['champion_winrate', 'champion_playrate']],
                id='col',
                value = 'champion_winrate',
                size='sm'
                ),
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(data=df_champion.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], span=12),
        dmc.Col([
            dcc.Graph(figure={}, id='graph')
        ], span=12),
    ]),
], fluid=True)

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='col', component_property='value')
)

def update_graph(col: str):
    fig = px.scatter(df_champion, x="champion_name", y=col, text="champion_name", log_x=False, size_max= 1)
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text=col, title_x=0.5)
    fig.update_layout(yaxis_range=[0,1])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)