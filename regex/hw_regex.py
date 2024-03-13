import requests
import re
from bs4 import BeautifulSoup
import html
import pandas as pd

class Hw:
    def __init__(self, path, file_name, url, working_url, header, cols):
        self.path = self.make_path(path)
        self.file_name = file_name
        self.file_path = self.path + self.file_name
        
        self.url = url
        self.working_url = self.url + working_url
        self.header = header
        self.cols = cols
        
    def make_path(self, path):
        foward_slash = ''
        if path[-1] != '/':
            foward_slash = '/'
        return path + foward_slash
    
    def display_file_path(self):
        print(f'File path: {self.file_path}.csv/html\n')
        
    def display_working_url(self):
        print(f'Url: {self.url}\nWorkin on url: {self.working_url}\n')

    def display_header(self):
        print('Header of the https request:')
        for key, value in self.header.items():
            print(f'{key}: {value}')
        print()
            
def fetch_data(url, header):
    try:
        response = requests.get(url, timeout=5, headers=header)
        response.raise_for_status()
        response.text
        return response.text
    except requests.RequestException as e:
        print(f"An HTTP request error occurred: {e}")
        return None

# strip tag using regex
def strip_tags_regex(html_content):
    tag_re = re.compile(r'<[^>]+>')
    plain_text = tag_re.sub('', html_content)
    return plain_text

# Not used
def strip_tags(html_str):
    # Use BeautifulSoup to parse and extract text without tags
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.get_text()

def clean_str(str):
    return str.replace('\t', '').replace('\n', '').replace('\r', '')

def clean_text(str):
    clean_lines = [line.strip() for line in str.split('\n') if line.strip()]
    return '\n'.join(clean_lines)

def clean_html(html_content):
    return clean_text(html.unescape(strip_tags_regex(html_content)))
               
# Fetch the data from website and put it into html file
def fetch_and_write_to_file(url, file_path, header):
    data = fetch_data(url, header)
    if data != None:
        with open(f"{file_path}.html", 'w') as html_file:
            html_file.write(data)

#debugging
def show_special_characters(text):
    # Replace new lines and tabs with their literal representations
    text = text.replace("\n", "\\n")
    text = text.replace("\t", "\\t")
    return text

# strip content tags and clean and format result
def get_clean_content(html_content):
    return clean_html(strip_tags_regex(html_content))

# return matches from regex
def parse_data(pattern, data):
    pattern = re.compile(rf'{pattern}', re.DOTALL |  re.IGNORECASE)
    match = re.findall(pattern, data)
    if match == []:
        return None
    return match

# use parse_data() and return None if no results, clean content otherwise
def get_content_from_regex(regex, data):
    content = parse_data(regex, data)
    if (content == None):
        return None
    return get_clean_content(content[0])

# Get link from regex
def get_link_from_regex(regex, data, pre_url):
    link_from_html = parse_data(regex, data)
    return pre_url + get_clean_content(link_from_html[0])

# Get ID from regex
def get_id_from_regex(regex, data):
    return parse_data(regex, data)[0]

# From multiple regex, get content and put it in a list of dictionary
def parse_ads(ads, url, cols):
    all_ads = []
    key_regexs = [
                    ('company', '<span data-cy="companyName".*?</span>'),
                    ('job_title', '<h3 class="!tw-mb-0">.*?</h3>'),
                    ('contract', '<span data-cy="contract".*?</span>'),
                    ('location', '<span class="tw-text-ellipsis.*?</span>'),
                    ('work_type', '<span data-cy="teleworkInfo">.*?</span>'),
                    ('salary', '<span data-cy="salaryInfo".*?</span>'),
                    ('posted_date', '<span data-cy="publishDate".*?</span>')
                ]
    
    for ad in ads:
        new_ad = {}
        link = get_link_from_regex('<a class="md:tw-text-xlOld.*?href="(.*?)"', ad, url)
        new_ad['id'] = get_id_from_regex('/(\d*).html$', link)
        for key_regex in key_regexs:
            new_ad[key_regex[0]] = get_content_from_regex(key_regex[1], ad)
        new_ad['link'] = link
        all_ads.append(new_ad)    
    return all_ads
    
# open file and get the html_content form it
def get_file_data(file_path):
    data = ""
    with open(f"{file_path}.html", 'r') as html_file:
        for line in html_file:
            # print(line, end='')
            data += line
    return data

def data_to_df(data):
    data = [ad.split('\n') for ad in data]
    for ad in data:
        print(ad)
        
def parse_simple_ads(ads):
    ret = [clean_html(line) for line in ads]
    return ret

def get_simple_df(ads):
    temp_cleaned_ads = parse_simple_ads(ads)
    data_to_df(temp_cleaned_ads)

# scrap data from local file hello_work.html in production mode
# change and make request by calling fetch_and_write_to_file(hw.working_url, 'hello_work', hw.header) to get the lattest update
def scrap(hw):
    # fetch_and_write_to_file(hw.working_url, hw.file_path, hw.header)
    file_data = get_file_data(hw.file_path)
    ads = parse_data('<div class="offer--content tw-rounded-2xl".*?<div class="highlights__container".*?>', file_data)
    data = parse_ads(ads, hw.url, hw.cols)
    # print(data)
    df = pd.DataFrame(data)
    df.to_csv(f'{hw.file_path}.csv', index=True)
    print(df)
    
    # data = get_simple_df(ads)
    # print(data)
    

