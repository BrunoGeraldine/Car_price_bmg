import re
import requests
import pandas        as pd

from bs4             import BeautifulSoup

list_auto = []

#Link do acesso
url = requests.get("https://www.autoscout24.com/lst/bmw?atype=C&cy=I&desc=0&fregfrom=2018&fregto=2022&powertype=kw&search_id=2ajkso6erxn&sort=standard&source=detailsearch&ustate=N%2CU")

#Salvando o objeto
content = url.content
url_final = []

#Convertendo para um objeto do tipo BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

list_auto = []

# Exemplo de uso:
def gerar_links_base(prefixo, sufixo, num_iteracoes, final_url):
    links = []

    for i in range(1, num_iteracoes + 1):
        link = f"{prefixo}{i}{sufixo}{final_url}"
        links.append(link)

    return links

# Exemplo de uso:
prefixo = "https://www.autoscout24.com/lst/bmw?atype=C&cy=I&desc=0&fregfrom=2018&fregto=2022&page="
sufixo = ""
num_iteracoes = 20
final_url = "&powertype=kw&search_id=2ajkso6erxn&sort=standard&source=listpage_pagination&ustate=N%2CU"

links_gerados = gerar_links_base(prefixo, sufixo, num_iteracoes, final_url)

for link in links_gerados:
    #print(link)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get( link )

    #Salvando o objeto
    content = page.content
    #url_final = []
    
    #Convertendo para um objeto do tipo BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Beautiful Soup object
    soup = BeautifulSoup( page.text, 'html.parser' )

    add = soup.find_all('article', re.compile('cldt-summary-full-item'))
     #Seller/Location
    seller_detail = soup.find('div', attrs={'class':re.compile('SellerInfo')})
    seller = seller_detail.find('span', attrs={'class':re.compile('SellerInfo_name')}).get_text().strip()
    endereco = seller_detail.find('span', attrs={'class':re.compile('SellerInfo_address')}).get_text().strip()

    for ads in add:
        auto = soup.find('a', attrs={'class':re.compile('ListItem_title')}).get_text().strip()
        id_ads = ads['id']
        manufacturer_by = ads['data-make']
        model = ads['data-model']
        year = ads['data-first-registration']
        km = ads['data-mileage']
        price = ads['data-price']
        description_car = ads.find('div', attrs={'class': re.compile("ListItem_wrapper")}).getText()
        version = ads.find('span', attrs={'class': re.compile("ListItem_version")}).getText()
        



        list_auto.append([id_ads, auto, manufacturer_by, 
                          model, year, km, price, description_car, 
                          version, seller, endereco])
        df = pd.DataFrame(list_auto, columns=["id_ads", "auto", "manufacturer_by", 
                                              "model", "year", "km", "price", "description_car", 
                                              "version", "seller", "endereco"])

rows = df.shape[0]
print(rows)
df.to_csv('../dataset/list_auto_paginacao.csv')

#df_gross = pd.read_csv('../dataset/list_auto_paginacao.csv')
#
#df_gross.to_excel('../dataset/list_auto_pag.xlsx', index=None, header=True)

######## ETL - Cleaning process

df_clean = pd.read_csv('../dataset/list_auto_paginacao.csv', encoding='utf-8', sep=';')

# "Extracting the postal code from the vehicle's country of origin. r'(\d+)
# Applying Regex for data cleaning."
df_clean['zip_code'] = df_clean['address'].apply(lambda x: int(re.search('\d+', x).group(0) if pd.notnull( x ) else x ))

# Country
df_clean['city'] = df_clean['address'].apply(lambda x: str(re.search('(?<=IT-\d{5}\s)\w+', x).group(0) if pd.notnull( x ) else x ))

# DataTime cleaning
df_clean['year'] = df_clean['year'].str.replace('-', '/')

for i in range(len(df_clean)):
    if df_clean['year'][i] == 'new' or df_clean['year'][i] == 'unknown' or df_clean['year'][i] == 'None':
        df_clean.at[i, 'year'] = '01/2023'

df_clean['year'] = pd.to_datetime(df_clean['year'], format='%m/%Y')
df_clean['year'] = df_clean['year'].dt.year

df_final = pd.DataFrame(df_clean[['id_ads', 'manufacturer_by', 'model', 'version', 'km', 'year',
                                  'price', 'seller', 'address', 'scrapy_datetime', 'zip_code', 'city']])


rows = df_final.shape[0]
print(rows)
df_final.to_csv('../dataset/df_cleaned.csv', encoding='utf-8', sep=';')

