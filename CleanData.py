import pandas as pd
import os
import csv

def clean_data(csv_path : str):
    premier_matches = pd.read_csv(csv_path)
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
    return rolling_matches
    
def rolling_avg(group, cols, new_cols):
    # Sort matches by date to calculate rolling averages
    group = group.sort_values("Date")
    rolling = group[cols].rolling(3, closed='left').mean()
    # Create new col for the rolling average, ignoring N/A results
    group[new_cols] = rolling
    group = group.dropna(subset=new_cols)
    return group

def write_new_data(csv_path, cleaned_data):
    with open(csv_path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_data)

def main():
    csv_path = os.getcwd() + "/webscrape/premier_league_2023-2024.csv"
    cleaned_data = clean_data(csv_path)
    write_new_data(csv_path, cleaned_data)
    
if __name__ == '__main__':
    main()
    