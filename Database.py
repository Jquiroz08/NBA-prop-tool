import pandas as pd
import os
import glob
import math

folderPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Players"
variables = ['PTS','TRB','AST','PRA','PA','PR','RA','3P']
dictonaryOfTeams={}

# Creates database to retrieve data from
def initilizeDatabase():
    # For loop which goes through each team folder in "Player" folder
    for teamName in os.listdir(folderPath):
        # Creates path to team folder
        filePath = os.path.join(folderPath, teamName)
        # Creates a nested dictionary where the Key is the team name and the value
        # is another dictonary of player data
        dictonaryOfTeams[teamName] = createPlayerDictionary(filePath)
        
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
                playerData[playerName] = df
            except Exception as e:
                print(f"Error reading {playerName}: {e}")
    return playerData

# Prints the hit rate of player props with a given line
def findStreak(teamName, playerName):
    # Reverses the data frame
    playerData = dictonaryOfTeams[teamName][playerName][::-1]
    # Itterates each collumn
    for i in variables:
        streakCount = 0
        strikeCount = 0
        totalGames = 0
        targetValue = math.ceil(playerData[i].mean() * 0.8)
        for j in playerData.index:
            if strikeCount > 2:
                print(playerName +" has a had " + str(targetValue) + " " + i + " in " + str(streakCount) + " of " + str(totalGames) + " games")
                break
            elif(playerData.loc[j,i]< targetValue):
                 strikeCount +=1
                 totalGames += 1 
            else:
                 streakCount += 1
                 totalGames += 1
        
    
initilizeDatabase()
#findStreak("OKC","Jalen Williams")
#print("---------------------")
#findStreak("CLE", "Donovan Mitchell")


