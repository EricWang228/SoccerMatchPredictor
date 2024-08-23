import csv
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 
from sklearn.metrics import precision_score

def clean_data(path : str) -> list:
    premier_matches = pd.read_csv(os.getcwd() + path)
    
    # Remove unused columns
    del premier_matches["Match Report"]
    del premier_matches["Notes"]
    
    # Convert columns to numeric data values for ML algorithms
    premier_matches["Date"] = pd.to_datetime(premier_matches["Date"])
    premier_matches['target'] = premier_matches["Result"].astype('category').cat.codes
    
    # The venue type (home/away) and opponent can be a strong predictor of a team's performance
    premier_matches['venue_code'] = premier_matches['Venue'].astype('category').cat.codes
    premier_matches['op_codes'] = premier_matches['Opponent'].astype('category').cat.codes
    
    # Rolling averages for xG and Poss
    cols = ["xG", "Poss"]
    # Add "_rolling" to all values in cols
    new_cols = [f"{col}_rolling" for col in cols]
    # Group all matches for each team and apply the rolling average func to each group  
    rolling_matches = premier_matches.groupby('Team').apply(lambda x: rolling_avg(x,cols,new_cols), include_groups=False)
    return rolling_matches.droplevel('Team')

def predict(premier_matches : list, prev_year : list):
    # Create a Random Forest Model
    rf = RandomForestClassifier(n_estimators=200, min_samples_split=10, random_state=1)
    # Predictors and training data
    predictors = ["venue_code", "op_codes", "Poss", "xG", "xGA", "xG_rolling", "Poss_rolling"]
    train_set = prev_year
    test_set = premier_matches 
    
    # Fit the random forest model
    rf.fit(train_set[predictors], train_set['target'])
    prediction = rf.predict(test_set[predictors])
    
    # Compare the fitted model with the actual results of the game
    compared = pd.DataFrame(dict(actual=test_set['target'], predicted=prediction), index=test_set.index)
    
    # Compute the accuracy of the model with the actual results
    error = accuracy_score(test_set['target'], prediction)
    return compared, error
    
def rolling_avg(group, cols, new_cols):
    # Sort matches by date to calculate rolling averages
    group = group.sort_values("Date")
    rolling = group[cols].rolling(3, closed='left').mean()
    # Create new col for the rolling average, ignoring N/A results
    group[new_cols] = rolling
    group = group.dropna(subset=new_cols)
    return group

def main():
    matches = clean_data("/webscrape/premier_league_2023-2024.csv")
    prev_year = clean_data("/webscrape/premier_league_2022-2023.csv")
    predictions, err = predict(matches, prev_year)
    print(err)
    print(predictions)
    
if __name__ == '__main__':
    main()