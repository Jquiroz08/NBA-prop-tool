import pandas as pd
import os
import glob
import math
import pickle

folderPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Players"

columnOrder = ['G','Tm', 'Opp', 'PTS', 'TRB', 'AST', 'PRA', 'PA', 'PR', 'RA', '3P']

dictonaryOfTeams={}
listOfTeamNames = []

# Creates database to retrieve data from
def initilizeDatabase():
    # For loop which goes through each team folder in "Player" folder
    for teamName in os.listdir(folderPath):
        # Creates path to team folder
        filePath = os.path.join(folderPath, teamName)
        # Creates a nested dictionary where the Key is the team name and the value
        # is another dictonary of player data
        listOfTeamNames.append(teamName)
        dictonaryOfTeams[teamName] = createPlayerDictionary(filePath)
    with open("teamDictionary.pkl", "wb") as f:
        pickle.dump(dictonaryOfTeams, f)
    
    with open("teamNames.pkl", "wb") as f:
        pickle.dump(listOfTeamNames, f)  
         
# Returns a dictionary where the key is the player name and the value is
# a data frame of the player stats
def createPlayerDictionary(filePath):
    playerData = {}
    # For loop which goes through each player excel file in the team folder
    for playerName in os.listdir(filePath):
         # Checks if it is '.xls' file
        if playerName.endswith(('.xls')):
            # Creates path to xls file
            currentFilePath = os.path.join(filePath, playerName)
            # Creates the key for the dictionary, which is the player's name
            playerName = playerName.replace(".xls","") 
            try:
                # Creates dataframe keeping certain collumns
                df = pd.read_excel(currentFilePath, engine='xlrd', usecols=['G','Tm','Opp','3P','TRB','AST','PTS'])
                # Only keeps data for games they played
                df = df[df['G'] >= 0]
                # Adds addtional collumns of data
                df['PRA'] = df['PTS'] + df['TRB'] + df['AST']
                df['PR'] =  df['PTS'] + df['TRB']
                df['PA'] =  df['PTS'] + df['AST']
                df['RA'] =  df['TRB'] + df['AST']
                df = df[columnOrder]
                df.reset_index(drop=True, inplace=True)
                playerData[playerName] = df
            except Exception as e:
                print(f"Error reading {playerName}: {e}")
    return playerData

initilizeDatabase()


