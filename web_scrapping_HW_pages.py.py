#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[23]:


base_url ='https://www.hellowork.com/fr-fr/emploi/recherche.html?k=data+analyst&l=lyon&l_autocomplete=lyon&ray=20&cod=all&d=all&page=3&p=1&mode=pagination'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://www.hellowork.com/fr-fr/emploi.html',
}


# In[24]:


emploi_data = []


# In[26]:


for page_num in range(1, 4):
    url = f'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=data+analyst&l=lyon&l_autocomplete=lyon&ray=20&cod=all&d=all&page=3&p={page_num}&mode=pagination'
    print(url)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        emplois = soup.select('ul.crushed li')

        for emploi in emplois:
            metadata_div_intitule = emploi.find('h3')
            intitule_poste = metadata_div_intitule.text.strip() if metadata_div_intitule else None

            metadata_div_entreprise = emploi.find('span', class_='tw-mr-2')
            entreprise = metadata_div_entreprise.text.strip() if metadata_div_entreprise else None

            metadata_div_type = emploi.find('span', class_='tw-w-max')
            emploi_type = metadata_div_type.text.strip() if metadata_div_type else None

            metadata_div_loc = emploi.find('span', class_='tw-text-ellipsis')
            location = metadata_div_loc.text.strip() if metadata_div_loc else None

            emploi_data.append({
                "Intitule Poste": intitule_poste,
                "Entreprise": entreprise,
                "Type": emploi_type,
                "Loc": location
            })

df_emploi = pd.DataFrame(emploi_data)


# In[ ]:




