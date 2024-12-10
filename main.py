import requests
from bs4 import BeautifulSoup
import json

def parse_url(url):
    response = requests.get(url)
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')

    message = soup.find('div', class_='doc-content')
    table = message.find('table')
   
    if table:
        print(table.prettify())
    else:
        raise ValueError("No table found in the document")

    parsed_data = []

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        # print(f"Extracted cells: {len(cells)}")
        if len(cells) == 3:
            x = cells[0].get_text(strip = True)
            character = cells[1].get_text(strip = True)
            y = cells[2].get_text(strip = True)
            parsed_data.append({
                'x':x,
                'character': character,
                'y': y,
            })

    json_output = json.dumps(parsed_data, indent = 4)
    
    sorted_data = sorted(parsed_data, key=lambda item:(int(item['x']), int(item['y'])))
    
    print(json.dumps(parsed_data, indent = 4, ensure_ascii=False))

    width = max(int(item['x']) for item in sorted_data) + 1
    height = max(int(item['y']) for item in sorted_data) + 1

    grid = [['' for _ in range(width)] for _ in range(height)]

    for item in sorted_data:
        x=int(item['x'])
        y=int(item['y'])
        grid[height - y - 1][x] = item['character']

    for row in grid:
        print(''.join(row))
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

parse_url(url)

# try:
#   table_data = parse_url(url)
#   for row in table_data:
#     print(row)
# except Exception as e:
#   print(f"Error: {e}")