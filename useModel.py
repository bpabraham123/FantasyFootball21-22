import pandas as pd

# This function takes a positional model, a csv file, and a position (QB, RB,
# WR, or TE) as parameters. It uses the model to predict a players stats, and
# it returns a dataframe.
def useModel(model, file, position):
    df = pd.read_csv(file)
    df.dropna()
    # checks where the Fant Pos is the position given and returns a data frame
    # with only the rows that include said position
    df = df[df['FantPos'] == position]

    # the model will use difference parameters based on position
    if position == 'QB':
        X = df[['PassAtt/G','PassYds/G', 'PassTD/G', 'RushAtt/G', 'Y/A',
                'RushYds/G', 'RushTD/G', 'TotTD/G','PPG','VBD']]
    elif position == 'RB':
        X = df[['Age', 'RushAtt/G', 'Y/A','RushYds/G', 'RushTD/G','Rec/G',
                'RecYds/G', 'Y/R', 'RecTD/G','TotTD/G','PPG','VBD']]
    elif position == 'WR' or 'TE':
        X = df[['Rec/G','RecYds/G','Y/R', 'RecTD/G','TotTD/G','PPG','VBD']]
    else:
        print('Invalid position entered')
        return
    yPred = model.predict(X)

    # creates new df with the name of player, their position, and their
    # predicted PPG
    dataFrameDict = {'Name': df['Player'], 'FantPos': df['FantPos'], 'Predicted PPG': yPred}
    dataFrame = pd.DataFrame(dataFrameDict)
    dataFrame = dataFrame.sort_values(by = ['Predicted PPG'], ascending = False)
    dataFrame['Predicted PPG'] = dataFrame['Predicted PPG'].round(decimals = 3)
    dataFrame['Predicted PPR'] = 17 * dataFrame['Predicted PPG']
    dataFrame['Predicted PPR'] = dataFrame['Predicted PPR'].round(decimals = 3)


     # this adds a position rank column to the dataframe
    posRank = []
    posRankNum = 1
    for index, row in df.iterrows():
        posRank.append(posRankNum)
        posRankNum += 1

    dataFrame['PosRank'] = posRank

    # this creates a VBD column (value based drafting)
    if position == 'QB':
        playersDrafted = 10 * 2
    if position == 'RB':
        playersDrafted = 10 * 4.5
    if position == 'WR':
        playersDrafted = 10 * 4.5
    if position == 'TE':
        playersDrafted = 10 * 2

    playersDrafted = playersDrafted
    newDF = dataFrame[dataFrame['PosRank'] == playersDrafted]
    baseline = newDF.iloc[0].at['Predicted PPR']
    dataFrame['VBD'] = dataFrame['Predicted PPR'] - baseline
    dataFrame['VBD'] = dataFrame['VBD'].round(decimals = 3)

    dataFrame = dataFrame.reset_index(drop = True)

    return dataFrame
