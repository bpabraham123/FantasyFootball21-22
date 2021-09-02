from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen


# This function takes an int as its input, where the input corresponds to a year
# after 1999. The function returns a pandas dataFrame of the scraped data
def scrape(year):
    url = "https://www.pro-football-reference.com/years/{}/fantasy.htm#".format(year)
    html = urlopen(url)
    #Creates a BeautifulSoup object
    soup = BeautifulSoup(html, features="lxml")


    headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
    headers = headers[1:]


    # finds all the rows that are not headers
    rows = soup.findAll('tr', class_= lambda table_rows: table_rows != "thead")
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
    player_stats = player_stats[2:]

    # creates an pandas dataframe object called stats
    stats = pd.DataFrame(player_stats, columns = headers)

    stats = stats.replace(r'', value=0, regex=True)
    stats['Year'] = year
    return stats


# This function takes two ints as its inputs, both of which correspond to a year
# after 1999. The function uses the scrape function to scrape the data from
# each year within that range. It then creates a pandas dataframe with all of
#the data, and it returns said dataframe.
def createDF(startYear, endYear):
    stats = pd.DataFrame()
    years = []
    # iterates through years specified
    for year in range(startYear, endYear + 1):
        years.append(year)
    for year in years:
        stats = stats.append(scrape(year))
    return stats

# This function cleans the data in the input dataframe by removing unneeded
# columns, renaming repeated columns, and adding columns. This function requires
# that the dataframe input was a dataframe made with the createDF() function.
# This function returns the cleaned dataframe.
def cleanDF(dataFrame):
    #edits df to not include unneeded statistics
    columnsToRemove = ['Tm', 'GS', 'Fmb', 'FL', '2PM', '2PP', 'DKPt', 'FDPt', 'FantPt']
    dataFrame = dataFrame.drop(columns = columnsToRemove)

    # Renames repeated columns
    cols = []
    ydsNum = 0
    tdNum = 0
    attNum = 0
    for column in dataFrame.columns:
        if column == 'Yds':
            if ydsNum == 0:
                cols.append('PassYds')
            elif ydsNum == 1:
                cols.append('RushYds')
            elif ydsNum == 2:
                cols.append('RecYds')
            ydsNum += 1
        elif column == 'Att':
            if attNum == 0:
                cols.append('PassAtt')
            elif attNum == 1:
                cols.append('RushAtt')
            attNum += 1
        elif column == 'TD':
            if tdNum == 0:
                cols.append('PassTD')
            elif tdNum == 1:
                cols.append('RushTD')
            elif tdNum == 2:
                cols.append('RecTD')
            elif tdNum == 3:
                cols.append('TotTD')
            tdNum += 1
        else:
            cols.append(column)

    dataFrame.columns = cols

    listOfColumns = ['Cmp', 'PassAtt' , 'PassYds', 'PassTD', 'Int',
                     'RushAtt', 'RushYds', 'RushTD', 'Tgt', 'Rec',
                     'RecYds', 'RecTD', 'TotTD']


    # Creates columns for stats per game
    for column in listOfColumns:
        newColumn = column + '/G'
        dataFrame[newColumn] = (pd.to_numeric(dataFrame[column]) / pd.to_numeric(dataFrame['G']))
        dataFrame[newColumn] = dataFrame[newColumn].round(decimals = 3)

    dataFrame = dataFrame.drop(columns = listOfColumns)

     # Creates column of points per game
    dataFrame['PPG'] = (pd.to_numeric(dataFrame['PPR']) / pd.to_numeric(dataFrame['G']))
    dataFrame['PPG'] = dataFrame['PPG'].round(decimals=3)


    # edits name for uniformity year over year
    dataFrame['Player'] = dataFrame.Player.str.replace('[^a-zA-Z]', '', regex = True)

    # creates unique player ID to make stats for different years easier to see
    playerID = []
    for index, row in dataFrame.iterrows():
        playerID.append(row['Player'] + str(row['Year']))
    dataFrame['ID'] = playerID

    # Sorts dataFrame to make it easier to find the value of the next year ppg
    dataFrame = dataFrame.sort_values(by = ['ID'], ascending = False)


    # Creates a list of the next year's PPG
    nextYearPPG = []
    lastPlayer = 'NaN'
    lastPlayerPPG = 'NaN'

    for index, row in dataFrame.iterrows():
        player = row['Player']
        if lastPlayer == player:
            nextYearPPG.append(lastPlayerPPG)
        else:
            nextYearPPG.append('NaN')
        lastPlayer = row['Player']
        lastPlayerPPG = row['PPG']

    dataFrame['Next Year PPG'] = nextYearPPG
    dataFrame = dataFrame.sort_values(by = ['ID'], ascending = True)
    dataFrame = dataFrame.reset_index(drop = True)
    return dataFrame


# This function takes a list of dataframes created with the createDF() function,
# and combines and sorts them and returns the new dataframe.
def combineData(listOfDataFrames):
    # creates a df which contains the dataframes in the list which is passed in
    df = pd.concat(listOfDataFrames)
    df = df.sort_values(by = ['Predicted PPR'], ascending = False)

    # gives players an overall ranking
    rankings = []
    rank = 1
    for index, row in df.iterrows():
        rankings.append(rank)
        rank += 1

    df['Ovr Rank'] = rankings

    df = df.reset_index(drop = True)
    return df
