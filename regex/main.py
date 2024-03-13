import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random

# url_job_city = "https://www.welcometothejungle.com/en/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=data%20analyst&page=1&aroundLatLng=45.75917%2C4.82965&aroundRadius=20&aroundQuery="
# example = 'https://example.com'
imdb_url = 'https://www.imdb.com/chart/top/'
 
def TEST():
     print('test')
 
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    # Add more user agents as needed
]

# List of proxies to rotate
PROXIES = [
    "http://proxy1.example.com",
    "http://proxy2.example.com",
    # Add more proxies as needed
]

 
def fetch_data(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    proxy = {"http": random.choice(PROXIES)}

    try:
        # Get request timeout of 5 seconds
        response = requests.get(url, timeout=5,  headers=headers, proxies=proxy)
        
        # Check the status code
        response.raise_for_status()
        response.text
        return response.text
    except requests.RequestException as e:
        # errors (e.g., connection refused, timeout exceeded, etc.)
        print(f"An HTTP request error occurred: {e}")
        return None

def clean_str(str):
    return str.replace('\t', '').replace('\n', '').replace('\r', '')

def strip_tags(html_str):
    # Use BeautifulSoup to parse and extract text without tags
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.get_text()    

def find_first(list, sub_str):
    for i, item in enumerate(list):
        if item.startswith(sub_str):
            return i
    return None

def parse_data(data, pattern):
    ret = None
    # data = "test, <rating> test </d>"
    pattern = re.compile(rf'{pattern}', re.IGNORECASE)
    match = re.findall(pattern, data)
    
    if match:
        ret = [strip_tags(line) for line in match]
        ret = [line for line in ret if line != '']
        first = find_first(ret, '1. ')
        last = find_first(ret, '250. ') + 2
        if first != None and last != None:
            ret = ret[first:last]
        ret = [ret[i:i+2] for i in range(0, len(ret), 2)]
    else:
        ret = ['No Info\n']
    return ret

def get_generated_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3) 
    
    html = driver.page_source
    driver.quit()
    return html

# def get_wttj(city, ctry):
#     return get_generated_data(url_job_city + f'{city}%2C%20{ctry}')

def data_to_html(data):
    html_content= """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        .movie-title {
            font-weight: bold;
        }
        .movie-year {
            color: #666;
        }
    </style>
</head>
<body>

<h1>Top 250 Movies</h1>

<ul>
    """
    for line in data:
        html_content += f'<li><span class="movie-title">{line[0]}</span> - <span class="movie-year">{line[1]}</span></li>'
        # print(line[0], ',', line[1])
    with open("movies.html", 'w') as html_file:
        html_file.write(html_content)

    html_content += """
</ul>

</body>
</html>
"""

def parse_img(data):
    # Parse the HTML
    soup = BeautifulSoup(data, 'lxml')
    
    images = soup.find_all('img')
    # Print out image info (src and alt attributes)
    # print(images)
    # for img in images:
    #     if img.get('alt', 'Tim Robbins in The Shawshank Redemption (1994)'):
    #         print(img['src'])
    # for img in images:
        # print(f"SRC: {img['src']}, ALT: {img.get('alt', 'No alt attribute')}")
    # print(images)
    
    for i, img in enumerate(images):
        alt = img.get('alt')
        if alt == 'Tim Robbins in The Shawshank Redemption (1994)':
            return i,
    return 0

def scrap():
    pattern = '<.*?title.*?>(.*?)</.*?>'
    pattern = '<div.*?>(.*?)</.*?>'
    
    # data = get_generated_data(imdb_url)
    data = fetch_data(imdb_url)
    print(data)
    # return
    # # # pattern = '<div.*?>(.*?)</.*?>'
    # # img = parse_img(data)
    
    # # parsed = strip_tags(data)
    parsed = parse_data(data, pattern)
    data_to_html(parsed)

def init_main():
    pass

def exit_main():
    pass

def main():
    init_main()
    scrap()
    exit_main()
    
if __name__ == "__main__":
    main()
