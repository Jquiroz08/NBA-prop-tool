import pandas as pd
import os
import glob
import math
import pickle


# Note: Rewrite function input methods to take string inputs instead of references to dataframes, as 
#       the keys and column names are all strings. So I am access the dataframes with
#       dictionaryOfTeams["Team Name"]["Player Name"], and read a column using
#       dictionaryOfTeams["Team Name"]['Player Name']["Column Name"]
#       It also makes the functions universal


folderPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Players"
boxScorePath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Box Scores"
propPath = r"C:\Users\josep\OneDrive\Desktop\Personal\NBA-prop-tool\Prop Lines.xls"


propLines = pd.read_excel(propPath, engine='xlrd',sheet_name= None)
variables = ['PTS','TRB','AST','PRA','PA','PR','RA','3P']
columnOrder = ['G','Tm', 'Opp', 'PTS', 'TRB', 'AST', 'PRA', 'PA', 'PR', 'RA', '3P']

with open("teamDictionary.pkl", "rb") as f:
    dictonaryOfTeams = pickle.load(f)

with open("teamNames.pkl", "rb") as f:
    listOfTeamNames = pickle.load(f)



# Prints the hit rate of player props with a given line
# Note: Rewrite to make more efficient in runtime
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
    while userInput !=5:
        menu()
        try:
            userInput = int(input())
            match userInput:
                case 1:
                    teamFinder()
                case 2:
                    updatePlayerStats()
                case 3:
                    propSearch()
                case 4:
                    sameGameParlay()
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
    print("1: Player Tool")
    print("2: Update with Box Scores" )
    print("3: Hit rate finder")
    print("4: Same Game Parlay Stats")
    print("5: Quit")  
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
        print(statData.loc[statData.index[i]].iloc[0])
        if statData.loc[statData.index[i]].iloc[0] >= line:
           count += 1
           
    print("He has had " + str(line) + " " + statData.keys()[0] + " in " + str(count) + " of 15 games")

# Gets the remaining prop values
def getMissingColumns(df):
    df['PRA'] = df['PTS'] + df['TRB'] + df['AST']
    df['PR'] =  df['PTS'] + df['TRB']
    df['PA'] =  df['PTS'] + df['AST']
    df['RA'] =  df['TRB'] + df['AST']
    return df

# Updates the player dataframe with the stats from their most recent game box score
# in the boxscore folder
def updatePlayerStats():
    for boxScore in os.listdir(boxScorePath):
        if boxScore.endswith(('.xls')):
            teamNames = boxScore.replace('.xls','')
            teamKey = teamNames[0:3]
            Opp = teamNames[4:7]
            currentFilePath = os.path.join(boxScorePath, boxScore)  
            df = pd.read_excel(currentFilePath, engine='xlrd', usecols=["Starters", "3P", "TRB", "AST", "PTS"])
            playerNames = df.pop("Starters")
            for i in range(len(df)):
                if playerNames[i] in  dictonaryOfTeams[teamKey]:
                    newRow = df.iloc[i]
                    newRow = getMissingColumns(newRow)
                    gameNumber = len(dictonaryOfTeams[teamKey][playerNames[i]]) + 1
                    newRow['Tm'] = teamKey
                    newRow['Opp'] = Opp
                    newRow['G'] = gameNumber
                    newRow = newRow[columnOrder]
                    dictonaryOfTeams[teamKey][playerNames[i]].loc[gameNumber - 1] = newRow
        os.remove(os.path.join(boxScorePath, boxScore))
    with open("teamDictionary.pkl", "wb") as f:
        pickle.dump(dictonaryOfTeams, f)
  
# Compares the entered prop lines in the excel file to the player stats in their database.
# Prints out the player and the props in the threshold
def propSearch(teams=propLines.keys(), threshold = 12):
    for teamName in teams:
        print(teamName)
        printLine()
        for i in range(len(propLines[teamName])):
            line = propLines[teamName].loc[i, 'Line']
            if math.isnan(line):
                continue
            playerName = propLines[teamName].loc[i, "Player"]
            stat = propLines[teamName].loc[i, "Stat"]
            data = dictonaryOfTeams[teamName][playerName][::-1].reset_index()
            count = 0
            for i in range(15):
                if data.loc[i,stat] >= line:
                    count += 1
            if count > threshold or count < 15 - threshold:
                print (playerName + " has hit " + str(line) + " " + stat + " in " + str(count) + " of 15 games")
        printLine()
            
def sameGameParlay():
  userInput = 0
  nameList = []
  for i in range(2):
    printLine()
    print(str(2-i) + " selections remaining")
    menu2()
    try:
        userInput = int(input())
        if(userInput == 31):
            break
        nameList.append(listOfTeamNames[userInput-1])
    except Exception as e:
            print("Please enter a valid number")  
  propSearch(nameList, 0)
   
    
runProgram()          

    


