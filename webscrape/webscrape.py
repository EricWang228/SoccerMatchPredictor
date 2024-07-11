from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import time

def get_team_premier_urls(team_urls):
    print("Grabbing Team Links!")
    team_premier_urls = []
    for team_url in team_urls:
        premier_req = Request(
            url = team_url,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
        team_webpage = urlopen(premier_req).read().decode("utf-8")
        soup = BeautifulSoup(team_webpage, 'html.parser')
    
        # Find and select the premier league from the scores and fixtures filter
        premier_link = soup.find_all('div', {'class' : 'filter'})[1]
        premier_link = premier_link.find_all('a')
    
        # Link for only the team's premier league games
        team_premier_urls.append("https://fbref.com" + premier_link[1].get("href"))
        time.sleep(3)
    print("Finished")
    return team_premier_urls
# Todo
def visit_team_premier_urls(premier_urls):
    # Visit the new link
    premier_req = Request(
        url = premier_link,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    premier_webpage = urlopen(premier_req).read().decode("utf-8")
    premier_soup = BeautifulSoup(premier_webpage, 'html.parser')
    
    # Find the scores and fixtures table & parse through it
    premier_table = premier_soup.find('table') 
    premier_table_headers = [headers.get_text(strip=True)for headers in premier_table.thead.find_all('th')]
    premier_table_data = []
    for row in premier_table.tbody.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text(strip=True))
        premier_table_data.append(row_data)
    
    return premier_table_headers + premier_table_data

# URL of the webpage to scrape
req = Request(
    url = 'https://fbref.com/en/comps/9/Premier-League-Stats',
    headers = {'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read().decode("utf-8")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')

# Find premier league team standing table 
premier_league_table = soup.find('table', {'class' : 'stats_table sortable min_width force_mobilize'})

# Extract all links from the table
links = premier_league_table.find_all('a')
links = [link.get("href") for link in links]

#  Remove links to the top team scorer, only team links remain
links = [link for link in links if '/en/squads/' in link]

# Add domain to team links
links = [f"https://fbref.com{link}" for link in links]

# Visit the team links
data = []

get_team_premier_urls(links)


# csv_file = 'premier_league_2023-2024.csv'
# Get the links for all teams
# print(f"Data has been successfully written to {csv_file}")
