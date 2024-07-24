from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import time
import os

def get_team_premier_urls(team_urls):
    print("Grabbing Team Links!")
    team_premier_urls = []
    for counter, team_url in enumerate(team_urls):
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
        print(counter, end=' ')
        time.sleep(3)
    print("\nFinished")
    return team_premier_urls

def get_header(team_link):
    premier_req = Request(
        url = team_link,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    premier_webpage = urlopen(premier_req).read().decode("utf-8")
    soup = BeautifulSoup(premier_webpage, 'html.parser')
    
    # Find the scores and fixtures table & parse the header information
    premier_table = soup.find('table') 
    premier_table_headers = [headers.get_text(strip=True)for headers in premier_table.thead.find_all('th')]
    premier_table_headers.append("Team")
    return premier_table_headers
    
def visit_team_premier_urls(premier_urls):
    premier_table_data = []
    print("Webscraping in progress")
    # Visits all links to premier league teams
    for counter, team in enumerate(premier_urls):
        # Visit the new link
        team_req = Request(
            url = team,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
        team_webpage = urlopen(team_req).read().decode("utf-8")
        soup = BeautifulSoup(team_webpage, 'html.parser')
        
        # Get the team name
        team_name = team.split('/')[-1].replace("-Scores-and-Fixtures-Premier-League", "").replace("-","")
        
        # Find the scores and fixtures table & parse through it
        premier_table = soup.find('table') 
        for row in premier_table.tbody.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.get_text(strip=True))
            row_data.append(team_name)
            premier_table_data.append(row_data)
        print(counter, end=' ')
        # Buffer to prevent too many requests sent at once
        time.sleep(3)
    print("\nFinished")
    return premier_table_data

def get_team_links(url: str) -> list:
    req = Request(
        url = url,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
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
    return links

def get_data_by_year(start_year: int, end_year: int):
    for year in range(start_year, end_year):
        print("Getting data for the {year1}-{year2} season".format(year1 = str(year), year2 = str(year + 1)))
        links = get_team_links('https://fbref.com/en/comps/9/{year1}-{year2}/{year1}-{year2}-Premier-League-Stats'.format(year1 = str(year),year2 = str(year + 1)))
        # Visit the team links
        data = []
        team_links = get_team_premier_urls(links)
        data.append(get_header(team_links[0]))
        time.sleep(20)
        data.append(visit_team_premier_urls(team_links))
        
        # Write data to csv file
        csv_file = os.getcwd() +'/premier_league_{year1}-{year2}.csv'.format(year1 = str(year), year2 = str(year+1))
        print(f"Writing data to {csv_file}")
        
        with open(csv_file, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(data[0]) 
            writer.writerows(data[1])

        print(f"Data has been successfully written to {csv_file}")
        time.sleep(60)
    return None
 
def main():   
    get_data_by_year(2021, 2024)

if __name__ == '__main__':
    main()