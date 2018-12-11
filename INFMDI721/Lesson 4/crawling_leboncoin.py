import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time

# Initialization of variables
# Need full header for Leboncoin crawling
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
           'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
           'Host': 'www.leboncoin.fr',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Upgrade-Insecure-Requests': '1',
           'Cookie': 'oas_ab=b; cto_lwid=fab9926a-3f1d-4bea-aa0e-c8e331775b81; xtvrn=$562498$; xtan562498=-undefined; xtant562498=1; _pulse2data=263c2fa2-ac27-4373-95e7-c66ea857e816%2Cv%2C%2C1544468187117%2CeyJpc3N1ZWRBdCI6IjIwMTgtMTItMTBUMTg6NDBaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..Csc4nWtMzZAseLJwZzu7Vg.2HiFeM0Xsy3BgjMwTnZS0KjceCS6RNh058CjelA81QeniN3J-3LqoJAZwReke6V_23i_B8jN0UDnDrGSriUQhAHEhtA5viVijEtg0gLlmrH_N3V7LprRT6O2youSU5lO0mt25NX9FWocqSmKl2ho8S6SZUMGFi229-ZOiHGujNUJrDNV36oxMrMywtro7Fb3GnsYfJEe1_98nWzzyxgBTw.VquL1BruQ7Hti7Eb1-M9wA%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..2wkDsnr_G0Xuxn4-zkkDCfLAbWm7QaFz4cFN0JPycUw; _scid=aea36670-d042-4bd6-94a9-d05ea341d9e0; euconsent=BOYkwMdOYkwMdAAAACFRBr-AAAAht7_______9______9uz_Gv_v_f__33e8__9v_l_7_-___u_-33d4-_1vX99yfm1-7ftr3tp_86ues2_Xur_959__njE; consent_allpurpose=cDE9MTtwMj0xO3AzPTE7cDQ9MTtwNT0x; cookieBanner=1; sq=ca=2_s; saveOnboarding=1; datadome=235f4bY-_XO0UhS2Ef02Q5.4Gc7JDiUea4RlqEmw1SA; ABTasty=uid%3D18121017091575840%26fst%3D1544458155117%26pst%3D1544458155117%26cst%3D1544467279188%26ns%3D2%26pvt%3D8%26pvis%3D7%26th%3D368617.476545.12.11.2.1.1544458155135.1544467800304.1; utag_main=v_id:016798e13a0e001eeda1a3a0503b03073001906b00978$_sn:2$_ss:0$_st:1544471908949'}
df = pd.DataFrame()
dict = {}
models = ['life', 'intens', 'zen'] # Different models of Renault ZOE
regions = ['2', '12', '21'] # Correspond to Aquitaine, IDF, PACA
list_model = []
list_region = []
list_seller_type = []
list_km = []
list_price = []
list_price_ref = []
list_lacentrale = np.zeros(3)


def _handle_request_result_and_build_soup(request_result):
    if request_result.status_code == 200:
        html_doc = request_result.content
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup


def get_price_ref(url):
    # Initialization
    res = requests.get(url)
    soup = _handle_request_result_and_build_soup(res)

    # Price ref
    price_ref_text = soup.find("strong", {"class", "bgRed sizeD"}).text
    regex_price = re.compile(r'\d+')
    price_formatted = re.findall(regex_price, price_ref_text)
    price_ref = int(''.join(price_formatted))
    return price_ref


def get_model_price_km_sellertype_phonenumber(url, region):
    # Initialization
    res = requests.get(url, headers=headers)
    soup = _handle_request_result_and_build_soup(res)
    i = 0
    # Search all offers
    offers = soup.find_all("li", {"class", "_3DFQ-"})
    for offer in offers:

        # Model
        title = offer.p.text
        if title.lower().find('life') != -1:
            list_price_ref.append(list_lacentrale[0])
            list_model.append('Life')
        elif title.lower().find('zen') != -1:
            list_price_ref.append(list_lacentrale[2])
            list_model.append('Zen')
        elif title.lower().find('intens') != -1:
            list_price_ref.append(list_lacentrale[1])
            list_model.append('Intens')
        else:
            list_price_ref.append('')
            list_model.append('')

        # seller Type
        category_class = offer.find("div", {"class", "_32V5I"})
        category = category_class.p.text
        if category.lower().find('pro') != -1:
            list_seller_type.append("Particulier")
        else:
            list_seller_type.append("Professionnel")

        # Price
        price_class = category_class.findNext('div')
        regex_price = re.compile(r'\d+')
        price_formatted = re.findall(regex_price, price_class.div.span.text)
        price = int(''.join(price_formatted))
        list_price.append(price)

        # Phone number
        # url_offer = 'https://www.leboncoin.fr' + offer.a['href']
        # req_post = requests.post(url=url_offer, headers=headers)
        # soup_post = _handle_request_result_and_build_soup(req_post)
        # phone_number_not_formatted = soup_post.find("a", {"class", "_2gotH _2ar1Z _1-5Yr"})
        # print(phone_number_not_formatted)

        # Km
        url_offer = 'https://www.leboncoin.fr' + offer.a['href']
        req_post = requests.post(url=url_offer, headers=headers)
        soup_post = _handle_request_result_and_build_soup(req_post)
        km_text = soup_post.find(text="Kilométrage").parent.findNext('div').text
        regex_km = re.compile(r'\d+')
        km_formatted = re.findall(regex_km, km_text)
        km = int(''.join(km_formatted))
        list_km.append(km)

        # Region
        list_region.append(region)

        # Try to bypass the verification system
        time.sleep(1)

    return list_region, list_price, list_model, list_km, list_seller_type, list_price_ref


i = 0
for model in models:
    url_la_centrale = 'https://www.lacentrale.fr/cote-auto-renault-zoe-q90+' + model + '+charge+rapide-2013.html'
    list_lacentrale[i] = get_price_ref(url_la_centrale)
    i += 1

for region in regions:
    url = "https://www.leboncoin.fr/recherche/?category=2&text=renault%20zoe&regions=" + region
    list_region_temp, list_price_temp, list_model_temp, list_km_temp, list_seller_type_temp, list_price_ref_temp = get_model_price_km_sellertype_phonenumber(url, region)
    list_model.append(list_region_temp)
    list_region.append(list_region_temp)
    list_seller_type.append(list_seller_type_temp)
    list_km.append(list_km_temp)
    list_price.append(list_price_temp)
    list_price_ref.append(list_price_ref_temp)

# Stockage des données dans un data frame
dict['Model'] = list_model
dict['Region'] = list_region
dict['Seller_Type'] = list_seller_type
dict['Km'] = list_km
dict['Price'] = list_price
dict['Price_ref'] = list_price_ref
df = pd.DataFrame.from_dict(dict)
df.head(300)
