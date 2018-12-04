import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#Paramétrage des variables
website = "https://www.open-medicaments.fr/api/v1/medicaments?query=parac%C3%A9tamol&api_key=paracetamol"


def _handle_request_result_and_build_soup(request_result):
    if request_result.status_code == 200:
        html_doc = request_result.content
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup


def get_medicines(url_page):
    get_req = requests.get(url_page).json()
    pd.DataFrame(get_req).head(10)
    # df = json.loads(get_req.content)
    # listcontrib = []
    # for i in range(1, 257):
    #     number = "#" + str(i)
    #     namecontrib = soup.find(text=number).parent.findNext('td').text
    #     listcontrib.append(namecontrib)
    # print(get_req)
    string = "PARACETAMOL ISOMED 1000 mg, comprimé"
    # reg = r',([\w\s*)'
    # re.findall(reg,string)


def reformat_req(longname):
    position = longname.find("(")
    return(longname[:position - 1])


get_medicines(website)




