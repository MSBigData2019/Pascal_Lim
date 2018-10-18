import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

#Paramétrage des variables
website = "https://gist.github.com/paulmillr/2657075"
head = {'Authorization': 'token {}'.format('mettre votre token')}


def _handle_request_result_and_build_soup(request_result):
    if request_result.status_code == 200:
        html_doc = request_result.content
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup


def get_top_contributors(url_page):
    res = requests.get(url_page)
    soup = _handle_request_result_and_build_soup(res)
    listcontrib = []
    for i in range(1, 257):
        number = "#" + str(i)
        namecontrib = soup.find(text=number).parent.findNext('td').text
        listcontrib.append(namecontrib)
    return listcontrib


def real_user_name(longname):
    position = longname.find("(")
    return(longname[:position - 1])


def get_mean_stars_users(listcontrib):
    #Initialisation des variables
    dico_mean_stars = {}
    list_stars_mean = []

    listcontrib_user_name = list(map(real_user_name,listcontrib))
    dico_mean_stars["login"] = listcontrib_user_name

    for i in range(len(listcontrib_user_name)):
        sum_stars = 0
        mean_stars = 0
        get_repo = requests.get("https://api.github.com/users/" + listcontrib_user_name[i] + "/repos", headers=head)
        get_json = json.loads(get_repo.content)
        for j in range(len(get_json)):
            sum_stars += get_json[j].get("stargazers_count")
        mean_stars = sum_stars/len(get_json)
        list_stars_mean.append(mean_stars)
        dico_mean_stars["mean"] = list_stars_mean

    df_users_stars_mean = pd.DataFrame.from_dict(dico_mean_stars)
    # print(df_users_stars_mean)
    print(len(get_json))

def get_mean_stars_user(user):
    user_name = user
    dico_mean_stars = {}
    sum_stars = 0
    mean_stars = 0
    get_repo = requests.get("https://api.github.com/users/" + user_name + "/repos", headers = head)
    get_json = json.loads(get_repo.content)
    for j in range(len(get_json)):
        sum_stars += get_json[j].get("stargazers_count")
    mean_stars = sum_stars/len(get_json)
    dico_mean_stars[user_name] = mean_stars
    # df_users_stars_mean = pd.DataFrame(dico_mean_stars.items(), columns=["user", "mean_stars"])
    print(dico_mean_stars)
    # print(df_users_stars_mean)


# listcontrib = get_top_contributors(website)
get_mean_stars_users(["fabpot ()"   ])
# get_mean_stars_user("fabpot")
