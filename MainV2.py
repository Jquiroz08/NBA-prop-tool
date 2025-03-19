import nba_api.stats.endpoints as API
from nba_api.stats.static import players , teams
import pandas as pd
import math
import time

propPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Prop Lines.xls"
propLines = pd.read_excel(propPath, engine='xlrd',sheet_name= None)
playerList = players.get_active_players()

propDictionary = {}
testString = ["MIL","POR","IND","ORL"]

def createPropDictionary():
    for teamName in propLines.keys():
        for i in range(len(propLines[teamName])):
            playerName = propLines[teamName].loc[i, "Player"]
            if playerName not in propDictionary.keys():
                propDictionary[playerName] = propLines[teamName].loc[propLines[teamName]["Player"] == playerName,["Stat","Line","Odds"]].reset_index()

def streakFinder():
    streakList = pd.DataFrame(columns=["Name","Stat","Line","Average","Streak","Odds"])
    streakIndex = 0
    for teamName in testString:
        teamID = teams.find_team_by_abbreviation(teamName)["id"]
        for playerName in API.CommonTeamRoster(team_id = teamID).get_data_frames()[0]["PLAYER"]:
            if playerName in propDictionary.keys():
                time.sleep(.700)
                playerId = [player for player in playerList if player['full_name'] == playerName][0]["id"]
                data = pd.DataFrame(API.PlayerGameLog(player_id=playerId,season_type_all_star="Regular Season",season=2024).get_data_frames()[0],columns=["PTS","REB","AST","FG3M"])
                data['PRA'] = data['PTS'] + data['REB'] + data['AST']
                data['PR'] =  data['PTS'] + data['REB']
                data['PA'] =  data['PTS'] + data['AST']
                data['RA'] =  data['REB'] + data['AST']
                for i in range(len(propDictionary[playerName])):
                    line = propDictionary[playerName].loc[i, 'Line']
                    if math.isnan(line):
                        continue
                    stat = propDictionary[playerName].loc[i, "Stat"]
                    odds = propDictionary[playerName].loc[i, "Odds"]
                    streakLength = 1
                    index = 0
                    over = data.loc[index,stat] >= line
                    under = data.loc[index,stat] < line
                    while over and index < len(data) - 1:
                        index = index + 1
                        over = data.loc[index,stat] >= line
                        if over:
                            streakLength = streakLength + 1
                    while under and index < len(data) - 1:
                        index = index + 1
                        under = data.loc[index,stat] < line
                        if under:
                            streakLength = streakLength + 1
                    if streakLength >= 2:
                        streakList.loc[streakIndex] = [playerName,stat,line,round(data.loc[:streakLength , stat].mean(),2),streakLength,odds]
                        streakIndex = streakIndex + 1
    new = streakList.sort_values(by=['Streak',"Odds"], ascending=False)
    print(new.head(60))

createPropDictionary()
streakFinder()




 