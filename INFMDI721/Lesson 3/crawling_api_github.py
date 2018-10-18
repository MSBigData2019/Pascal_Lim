import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

#Paramétrage des variables
website = "https://gist.github.com/paulmillr/2657075"
head = {'Authorization': 'token {}'.format('4ff5d101d25d4057916fcfeaa3d704041cd591e5')}


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
    #Récupération de la liste formatée des users et insertion dans un dictionnaire
    listcontrib_user_name = list(map(real_user_name,listcontrib))
    dico_mean_stars["login"] = listcontrib_user_name
    #Récupération de la moyenne de stars de tous les repos de chaque user
    for i in range(len(listcontrib_user_name)):
        sum_stars = 0
        mean_stars = 0
        get_nbrepo = requests.get("https://api.github.com/users/" + str(listcontrib_user_name[i]), headers=head)
        nb_repo = json.loads(get_nbrepo.content).get("public_repos")
        # Prise en compte du cas où l'utilisateur n'a pas de repo
        if nb_repo == 0:
            mean_stars = 0
        else:
            page = 1
            get_repo = requests.get("https://api.github.com/users/" + listcontrib_user_name[i] +
                                    "/repos?perpage=100&page=" + str(page), headers=head)
            repo_page = json.loads(get_repo.content)
            #On cherche à calculaer la somme de tous les stars en prenant en comtpe la pagination
            while repo_page != []: #le contenu du get est une liste vide lorsque la page ne contient pas de repos
                for j in range(len(repo_page)):
                    sum_stars += repo_page[j].get("stargazers_count")
                page += 1
                get_repo = requests.get("https://api.github.com/users/" + listcontrib_user_name[i] +
                                        "/repos?perpage=100&page=" + str(page), headers=head)
                repo_page = json.loads(get_repo.content)
            mean_stars = sum_stars/nb_repo
        list_stars_mean.append(mean_stars)
    #Mise en place dans le dictionnaire des moyennes de stars de chaque utilisateur
    dico_mean_stars["mean"] = list_stars_mean
    df_users_stars_mean = pd.DataFrame.from_dict(dico_mean_stars)
    print(df_users_stars_mean.sort_values(["mean"], ascending=False))


listcontrib = get_top_contributors(website)
get_mean_stars_users(listcontrib)
