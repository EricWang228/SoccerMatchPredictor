import csv
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 
from sklearn.metrics import precision_score

def clean_data() -> list:
    premier_matches = pd.read_csv(os.getcwd() + "/webscrape/premier_league_2023-2024.csv")
    
    # Remove unused columns
    del premier_matches["Match Report"]
    del premier_matches["Notes"]
    
    # Convert columns to numeric data values for ML algorithms
    premier_matches["Date"] = pd.to_datetime(premier_matches["Date"])
    premier_matches['target'] = premier_matches["Result"].astype('category').cat.codes
    
    # The venue type (home/away) and opponent can be a strong predictor of a team's performance
    premier_matches['venue_code'] = premier_matches['Venue'].astype('category').cat.codes
    premier_matches['op_codes'] = premier_matches['Opponent'].astype('category').cat.codes
    
    return premier_matches

def predict(premier_matches : list):
    # Create a Random Forest Model
    rf = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
    # Predictors and training data
    predictors = ["venue_code", "op_codes", "Poss", "xG", "xGA"]
    train_set = premier_matches[premier_matches['Date'] < '2023-12-28']
    test_set = premier_matches[premier_matches['Date'] > '2023-12-28']
    
    # Fit the random forest model
    rf.fit(train_set[predictors], train_set['target'])
    prediction = rf.predict(test_set[predictors])
    
    # Compare the fitted model with the actual results of the game
    compared = pd.DataFrame(dict(actual=test_set['target'], predicted=prediction), index=test_set.index)
    
    # Compute the accuracy of the model with the actual results
    error = accuracy_score(test_set['target'], prediction)
    return compared, error
    
    
def main():
    premier_matches = clean_data()
    predictions, err = predict(premier_matches)
    print(err)
    print(predictions)
    
if __name__ == '__main__':
    main()