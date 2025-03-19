import nba_api.stats.endpoints as API
from nba_api.stats.static import players , teams
import pandas as pd
import math
import time

propPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Prop Lines.xls"
propLines = pd.read_excel(propPath, engine='xlrd',sheet_name= None)
playerList = players.get_active_players()

def streakFinder():
    streakList = pd.DataFrame(columns=["Name","Stat","Line","Average","Streak","Odds"])
    streakIndex = 0
    teamName = "POR"
    for i in range(70):
        line = propLines[teamName].loc[i, 'Line']
        if math.isnan(line):
                continue
        playerName = propLines[teamName].loc[i, "Player"]
        stat = propLines[teamName].loc[i, "Stat"]
        time.sleep(.750)
        playerId = [player for player in playerList if player['full_name'] == playerName][0]["id"]
        data = pd.DataFrame(API.PlayerGameLog(player_id=playerId,season_type_all_star="Regular Season",season=2024).get_data_frames()[0],columns=["PTS","REB","AST","FG3M"])
        data['PRA'] = data['PTS'] + data['REB'] + data['AST']
        data['PR'] =  data['PTS'] + data['REB']
        data['PA'] =  data['PTS'] + data['AST']
        data['RA'] =  data['REB'] + data['AST']
        odds = propLines[teamName].loc[i, "Odds"]
        streakLength = 1
        index = 0
        over = data.loc[index,stat] >= line
        under = data.loc[index,stat] < line
        while over:
            index = index + 1
            over = data.loc[index,stat] >= line
            if over:
                streakLength = streakLength + 1
        while under:
            index = index + 1
            under = data.loc[index,stat] < line
            if under:
                streakLength = streakLength + 1
        if streakLength >= 2:
            streakList.loc[streakIndex] = [playerName,stat,line,round(data.loc[:streakLength , stat].mean(),2),streakLength,odds]
            streakIndex = streakIndex + 1
    new = streakList.sort_values(by=['Streak',"Odds"], ascending=False)
    print(new.head(60))

streakFinder()






 