import pandas as pd
import os
import glob
import math

numberOfDataFrames = 5
streakCount = 0
variables = ['PTS','TRB','AST','PRA','PA','PR','RA','3P']
storedData = []

ATL = {}
CLE = {}
BOS = {}
OKC = {}
MIN = {}

listOfTeams = [OKC , MIN]

folderPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Players"

# Assigns the player data to their respective team dictionary
def findTeam(teamName, playerName, dataFrame = None):
    match teamName:
        case "ATL":
            ATL[playerName] = dataFrame
        case "BOS": 
            BOS[playerName] = dataFrame
        case "CLE":
            CLE[playerName] = dataFrame
        case "OKC":
            OKC[playerName] = dataFrame
        case "MIN":
            MIN[playerName] = dataFrame
        case " _":
            print("Something went wrong")
          
# Reads the player excel file and create a dataframe of it            
def createDataFrame(path, folderName):
    for playerName in os.listdir(path): # For loop which goes through each file in folder
        if playerName.endswith(('.xls')): # Checks if it is '.xls' file
            filePath = os.path.join(path, playerName) # Creates path to xls file
            playerName = playerName.replace(".xls","") # Creates the key for the dictionary, which is the player's name
            try: # Creates dataframe keeping certain collumns
             df = pd.read_excel(filePath, engine='xlrd', usecols=['G','Tm','Opp','3P','TRB','AST','PTS'])
             df = df[df['G'] >= 0] # Only keeps data for games they played
             df['PRA'] = df['PTS'] + df['TRB'] + df['AST']
             df['PR'] =  df['PTS'] + df['TRB']
             df['PA'] =  df['PTS'] + df['AST']
             df['RA'] =  df['TRB'] + df['AST']
             findTeam(folderName, playerName, df) # Assigns data to respective team dictionary
            except Exception as e:
                print(f"Error reading {playerName}: {e}")

# Scans the "Players" Folder, which has subfolders of each team
def folderScan(path):
    for folderTeamName in os.listdir(path): #For loop which goes through each team folder in "Player" folder
        filePath = os.path.join(path, folderTeamName) # Creates path to folder
        createDataFrame(filePath, folderTeamName) # Runs funtion to create dataframes for each xls file in team folder


def findStreak(playerData, playerName):
    playerData = playerData[::-1]
    for i in variables:
        streakCount = 0
        strikeCount = 0
        totalGames = 0
       # targetValue = math.ceil(playerData[i].mean() - playerData[i].std())
        targetValue = math.floor(playerData[i].mean()*0.9)
        for j in playerData.index:
            if strikeCount > 1:
                print(playerName +" has a had " + str(targetValue) + " " + i + " in " + str(streakCount) + " of " + str(totalGames) + " games")
                break
            elif(playerData.loc[j,i]< targetValue):
                 strikeCount +=1
                 totalGames += 1 
            else:
                 streakCount += 1
                 totalGames += 1

                             
folderScan(folderPath)


for team in listOfTeams:
    for player in team.keys():
        findStreak(team[player],player)


#EX = CLE["Darrius Garland"]
#print(MIN.keys())

#findStreak(EX)


