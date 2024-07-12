import csv
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier

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
    
def main():
    cleaned_matches = clean_data()
    
if __name__ == '__main__':
    main()