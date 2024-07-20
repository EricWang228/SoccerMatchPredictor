import csv
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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
def model(data : list):
    rf = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
    train = data
    predictors = ["venue_code", "op_codes", "Poss", "xG", "xGA"]
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(data[predictors])
    error = accuracy_score(data["target"], preds)
    combined = pd.DataFrame(dict(actual=data["target"], predicted=preds))
    print(pd.crosstab(index=combined["actual"], columns=combined["predicted"]))
    # print(combined)
    
def main():
    cleaned_matches = clean_data()
    model(cleaned_matches)
    
if __name__ == '__main__':
    main()