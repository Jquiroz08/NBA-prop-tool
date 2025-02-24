import pandas as pd
import os
import glob
import math

folderPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Players"
variables = ['PTS','TRB','AST','PRA','PA','PR','RA','3P']
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

# Runs the program to create the menu in the terminal     
def runProgram():
    userInput = 0
    while userInput != 2:
        menu()
        try:
            userInput = int(input())
            match userInput:
                case 1:
                    teamFinder()
                case _:
                    print("Invalid Option")
        except Exception as e:
            print("Please enter a valid number")    
    print('Goodbye')
    
def printLine():
     print("--------------------------------") 
     
def menu():
    printLine()
    print("Please select option") 
    print("1: Prop Tool")
    print("2: Quit")  
    printLine()
    
def menu2():
    printLine()
    print("Please select Team") 
    teamList()
    print("31: Back")  
    printLine()
 
def menu3(teamDictionary, lastOption):
    printLine()
    print("Please select a player")
    playerList(teamDictionary)
    print(str(lastOption) + ": Back")
    printLine()
    
def menu4():
    printLine()
    variableList()
    print("9: Back")
    printLine()

# Prints the prop categories
def variableList():
    for i in range(len(variables)):
        print(str(i+1) + ": " + variables[i]) 

# Prints the name of the teams
def teamList():
    for i in range(len(listOfTeamNames)):
        print(str(i+1) + ": " + listOfTeamNames[i])

# Prints the name of the players based on the team name key
def playerList(teamDictionary):
    for i in range(len(teamDictionary)):
        print(str(i+1) + ": " + list(teamDictionary)[i])

# Gets user selection for team names
def teamFinder():
    userInput = 0
    while userInput != 31:
        menu2()
        try:
           userInput = int(input())
           playerFinder(dictonaryOfTeams[listOfTeamNames[userInput-1]])
        except Exception as e:
            print("Please enter a valid number")     

# Gets user selection for player names
def playerFinder(teamDictionary):
    userInput = 0
    lastOption = len(teamDictionary) + 1
    while userInput != lastOption:
        menu3(teamDictionary, lastOption)
        try:
           userInput = int(input())
           playerData(teamDictionary[list(teamDictionary)[userInput-1]])
        except Exception as e:
            print("Please enter a valid number") 
   
# Gets user selection for prop category 
def playerData(playerDataFrame):
    userInput = 0
    while userInput != 9:
        menu4()
        try:
            userInput = int(input())
            manualPropFinder(playerDataFrame[[variables[userInput - 1]]])
        except Exception as e:
            print("Please enter a valid number") 

# Gets user input for prop line
def manualPropFinder(statData):
    statData = statData[::-1]
    printLine()
    print("Enter prop line for " + statData.keys()[0])
    userInput = int(input())
    singleColumnSearch(statData, userInput)

# Prints the amount of times the prop has hit in a certain amount of games
def singleColumnSearch(statData, line):
    count = 0
    for i in range(15):
        if statData.loc[statData.index[i]].iloc[0] > line:
           count += 1
           
    print("He has had " + str(line) + " " + statData.keys()[0] + " in " + str(count) + " of 15 games")
    
 
    
initilizeDatabase()

runProgram()


