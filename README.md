== Fantasy Football Points Predictor ==
  Contributor: bpabraham123 (Benjamin Abraham)
  Email: bpabraham123@gmail.com
  Requires at least: Python 3, bs4, pandas, urllib, and sklearn


== Description ==
    This program is designed to predict the fantasy football points of NFL Players
  for the upcoming 2021-2022 NFL Season. There are four python files contained
  within this program. The first of which is "editDF.py" which contains
  functions that will scrape pro-football-reference.com for data, clean said
  data, and create dataFrames and CSV's from the data. The second of which is
  "createModel.py". This file contains functions which will create machine
  learning models for each position and test those models on previous years'
  data. The third file is "useModel.py" which contains the function to apply
  the position models to current data and make predictions. Lastly, there is a
  "main.py" file which contains the main() function which runs the program.
  Additionally, there are several csv files in the program; "trainingData.csv",
  "testingData.csv", and "predictionData.csv". The first of these refers to the
  data which will train the model, the second refers to the data which will test
  the model, and the third refers to the data which will be used to make
  predictions for 2021. Additionally, there is a "predictedStats.csv" file and
  various positional stats csv files. These files contain predictions for the
  2021-2022 NFL Football season.
    I intend to improve upon this model in the future, so that it can account
  for many of the variables which may go unnoticed in this version. Things such
  as free agent signings, injuries, retirements, and rookies affect the league
  drastically, and my model, in its current state, is unaware of these. Some
  improvements I intend to make in future versions are a rookie stats predictor
  as well as predicting team stats and then what percent of that a given player
  may garner. Any other feedback would be greatly appreciated.
