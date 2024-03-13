from regex import hw_regex as rgx
from soup import web_scrapping_final as sp

def init_main():    
    path = 'regex/'
    file_name = 'hello_work'
    url = 'https://www.hellowork.com'
    working_url = '/fr-fr/emploi/recherche.html?k=Data+analyst&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FAnalyste_donnees&l=Lyon+69000&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fcommune%2F69123#47444193'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://www.hellowork.com/fr-fr/emploi.html',
    }
    cols = ('company', 'job_title', 'contract', 'location', 'work_type', 'salary', 'posted_date', 'link', 'id')
    
    hw = rgx.Hw(path, file_name, url, working_url, headers, cols)
    return hw

def exit_main():
    pass
    
# use the methode with beautifulsoup by Mathieu in order to scrap data analyst job ads
def hellowork_methode_soup():
    df = sp.scrape_hw()
    print(df)

# use the methode with regex by Adib in order to scrap data analyst job ads
def hellowork_methode_rgx(hw):
    rgx.scrap(hw)
    hw.display_file_path()
    hw.display_working_url()
    hw.display_header()

def put_separation(sep = '='):
    print('\n\n' + sep * 150 + '\n\n')

def main():
    hw = init_main()
    
    put_separation()
    
    # first methode beautifulsoup
    hellowork_methode_soup()
    
    put_separation()
    
    # second methode with regex
    hellowork_methode_rgx(hw)
    
    put_separation()
    
    exit_main()
    
if __name__ == "__main__":
    main()