import requests
from bs4 import BeautifulSoup

def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        raise ValueError("No table found in the document")

    rows = table.find_all('tr')
    parsed_data = []

    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) == 3:
            x = cells[0].get_text(strip = True)
            character = cells[1].get_text(strip = True)
            y = cells[2].get_text(strip = True)
            parsed_data.append({
                'x':int(x),
                'character': character,
                'y': int(y),
                
            })
            return parsed_data

url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

try:
  table_data = parse_url(url)
  for row in table_data:
    print(row)
except Exception as e:
  print(f"Error: {e}")