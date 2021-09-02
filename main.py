from editDF import cleanDF, createDF, combineData
from createModel import createPositionModel, testModel
from useModel import useModel
import pandas as pd

def main():
    #This disables warnings for setting with copy
    pd.options.mode.chained_assignment = None
    
    #Creates dataFrames
    trainingData1 = cleanDF(createDF(2000, 2016))
    trainingData2 = cleanDF(createDF(2017, 2020))
    testingData = cleanDF(createDF(2016, 2017))
    trainingData = pd.concat([trainingData1, trainingData2])
    useData = cleanDF(createDF(2020, 2020))
    
    trainingData.to_csv('trainingData.csv')
    testingData.to_csv('testingData.csv')
    useData.to_csv('predictionData.csv')
    
    
    # creates ML models from data by position
    qbModel = createPositionModel('trainingData.csv', 'QB')
    rbModel = createPositionModel('trainingData.csv', 'RB')
    wrModel = createPositionModel('trainingData.csv', 'WR')
    teModel = createPositionModel('trainingData.csv', 'TE')
    
    # tests models
    testModel(qbModel, 'testingData.csv', 'trainingData.csv', 'QB')
    testModel(rbModel, 'testingData.csv', 'trainingData.csv', 'RB')
    testModel(wrModel, 'testingData.csv', 'trainingData.csv', 'WR')
    testModel(teModel, 'testingData.csv', 'trainingData.csv', 'TE')
    
    # applies models to prediction data
    qbStats = useModel(qbModel, 'predictionData.csv', 'QB')
    rbStats = useModel(rbModel, 'predictionData.csv', 'RB')
    wrStats = useModel(wrModel, 'predictionData.csv', 'WR')
    teStats = useModel(teModel, 'predictionData.csv', 'TE')
    
    # creates a dataFrame of all the predicted data and converts it to a csv
    data = [qbStats, rbStats, wrStats, teStats]
    fullData = combineData(data)
    fullData.to_csv('predictedStats.csv')
    
    # creates positional csv files
    qbStats.to_csv('21QbStats.csv')
    rbStats.to_csv('21RbStats.csv')
    wrStats.to_csv('21WrStats.csv')
    teStats.to_csv('21TeStats.csv')
    
    
    
    
    
if __name__ == '__main__':
    main()