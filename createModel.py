from sklearn import linear_model
import pandas as pd

# This file takes an input of a csv file and a position (QB, RB, TE, or WR)
# It then uses linear regression to create a ML model to predict next year stats
def createPositionModel(file, position):
    # creates a df from the csvFile, drops na values and rows where FantPos
    # does not equal the position parameter
    df = pd.read_csv(file)
    df = df.dropna()
    df = df[df['FantPos'] == position]

    # the model will use different independent variables depending on position
    if position == 'QB':
        X = df[['PassAtt/G','PassYds/G', 'PassTD/G', 'RushAtt/G', 'Y/A','RushYds/G',
                    'RushTD/G', 'TotTD/G','PPG','VBD']]
    elif position == 'RB':
        X = df[['Age', 'RushAtt/G', 'Y/A','RushYds/G', 'RushTD/G','Rec/G','RecYds/G','Y/R',
                    'RecTD/G','TotTD/G','PPG','VBD']]
    elif position == 'WR' or 'TE':
        X = df[['Rec/G','RecYds/G','Y/R', 'RecTD/G','TotTD/G','PPG','VBD']]
    else:
        print('Invalid position entered')
        return

    y = df['Next Year PPG']
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    return regr

# This function tests the accuracy of a position model
# It takes a position model, a csv file, and a position (QB, RB, TE, or WR)
# as parameters
def testModelAccuracy(model, file, position):
    # creates a df from the csvFile, drops na values and rows where FantPos
    # does not equal the position parameter
    df = pd.read_csv(file)
    df = df.dropna()
    df = df[df['FantPos'] == position]

    # the model will use different independent variables depending on position
    if position == 'QB':
        XTest = df[['PassAtt/G','PassYds/G', 'PassTD/G', 'RushAtt/G', 'Y/A','RushYds/G',
                    'RushTD/G', 'TotTD/G','PPG','VBD']]
    elif position == 'RB':
        XTest = df[['Age', 'RushAtt/G', 'Y/A','RushYds/G', 'RushTD/G','Rec/G','RecYds/G','Y/R',
                    'RecTD/G','TotTD/G','PPG','VBD']]
    elif position == 'WR' or 'TE':
        XTest = df[['Rec/G','RecYds/G','Y/R', 'RecTD/G','TotTD/G','PPG','VBD']]
    else:
        print('Invalid position entered')
        return

    yTest = df['Next Year PPG']
    results = model.score(XTest, yTest)
    return results

# This function tests the difference between the predicted points and the
# actual points. It takes a positional model, a csv file, and a position
# (QB, RB, TE, or WR) as parameters. The function returns a dataframe,
# the mean and median differences, and the mean and meadian absolute differences
def testModelDifference(model, file, position):
    # creates a df from the csvFile, drops na values and rows where FantPos
    # does not equal the position parameter
    df = pd.read_csv(file)
    df = df.dropna()
    df = df[df['FantPos'] == position]

    # the model will use different independent variables depending on position
    if position == 'QB':
        XTest = df[['PassAtt/G','PassYds/G', 'PassTD/G', 'RushAtt/G', 'Y/A','RushYds/G',
                    'RushTD/G', 'TotTD/G','PPG','VBD']]
    elif position == 'RB':
        XTest = df[['Age', 'RushAtt/G', 'Y/A','RushYds/G', 'RushTD/G','Rec/G','RecYds/G','Y/R',
                    'RecTD/G','TotTD/G','PPG','VBD']]
    elif position == 'WR' or 'TE':
        XTest = df[['Rec/G','RecYds/G','Y/R', 'RecTD/G','TotTD/G','PPG','VBD']]
    else:
        print('Invalid position entered')
        return


    yPred = model.predict(XTest)
    predAndActual = {'Name': df['Player'], 'Predicted PPG': yPred,
                     'Actual PPG': df['Next Year PPG']}

    # creates df from dictionary above
    dataFrame = pd.DataFrame(predAndActual)

    # creates a difference column which depicts the difference between the
    # predicted PPG and actual PPG
    dataFrame['Predicted PPG'] = dataFrame['Predicted PPG'].round(decimals=3)
    dataFrame['Difference'] = dataFrame['Predicted PPG'] - dataFrame['Actual PPG']
    dataFrame['Difference'] = dataFrame['Difference'].round(decimals=3)
    dataFrame['AbsDifference'] = dataFrame['Difference'].abs()
    meanDiff = round(dataFrame['Difference'].mean(), 3)
    medianDiff = round(dataFrame['Difference'].median(), 3)
    meanAbsDiff = round(dataFrame['AbsDifference'].mean(), 3)
    medianAbsDiff = round(dataFrame['AbsDifference'].median(), 3)

    return dataFrame, meanDiff, medianDiff, meanAbsDiff, medianAbsDiff

# This function takes two csv files (one to test and one to train), a positional
# model, and a position (QB, RB, TE, or WR) as parameters. The function then
# runs both the testModelAccuracy() and testModelDifference() functions, and
# the function does not return any value.
def testModel(model, testCSV, trainingCSV, position):
    accuracy = testModelAccuracy(model, trainingCSV, position)
    differences = testModelDifference(model, testCSV, position)
    meanDiff = differences[1]
    medDiff = differences[2]
    meanAbsDiff = differences[3]
    medAbsDiff = differences[4]

    print('The accuracy of the {0} model is {1}'.format(position, accuracy))
    print('The {0} model has an average error of {1} PPG and an average absolute error of {2} PPG'.format(position, meanDiff, meanAbsDiff))
    print('The {0} model has a median error of {1} PPG and a median absolute error of {2} PPG'.format(position, medDiff, medAbsDiff))
    print('\n')
    return
