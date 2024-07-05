from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

# URL of the webpage to scrape
req = Request(
    url = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures',
    headers = {'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read().decode("utf-8")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')

# Find table of match data
table = soup.find('table', {'id': 'sched_2023-2024_9_1'})

# Find header row from the thead of the table
table_headers = []
for header in table.thead.find_all('th'):
    table_headers.append(header.get_text(strip=True))

# Find all tbody rows from the table
data = []
for row in table.tbody.find_all('tr'):
    if 'spacer' in row.get('class', []):
        continue
    row_data = []
    for cell in row.find_all(['th', 'td']):
        text = cell.get_text(strip=True)
        row_data.append(text)
    data.append(row_data)

# Write the data to a CSV file
csv_file = 'premier_league_2023-2024.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(table_headers)
    writer.writerows(data)

print(f"Data has been successfully written to {csv_file}")
