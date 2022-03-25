# TOM B IIM A3 WEB ALT 2
import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur"
page = requests.get(url)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")
    content = soup.find("div", id="content")

    ######## PREMIER TABLEAU ########

    standard_div = content.find("div", id="all_stats_standard")
    h2 = standard_div.find("h2")
    table = standard_div.find("table")
    first_header_row = table.find("tr", class_="over_header")
    second_header_row = first_header_row.find_next_sibling("tr")

    first_header_row = first_header_row.find_all("th")
    second_header_row = second_header_row.find_all("th")

    principal_header_title = []
    secondary_header_title = []
   
    secondary_header_title = ["Nom"]
    for i, header in enumerate(second_header_row):
        if i == 0:
            principal_header_title.append(header.text)
        else:
            secondary_header_title.append(header.text)
   
    for i, header in enumerate(first_header_row):
        principal_header_title.append(header.text)
       
    principal_header_title = [x for x in principal_header_title if x]

    for i, header in enumerate(principal_header_title):
        if principal_header_title.count(header) > 1:
            principal_header_title[i] += " " + str(principal_header_title.count(header))

    tableau_1 = []
    tr = table.select("tbody tr:not(.thead)")

    for i, row in enumerate(tr):
        row_main = {}
        row_list = []
        th = row.find("th")
        row_list.append(th.text)
        for j, td in enumerate(row.find_all("td")):
            row_list.append(td.text)
            if j == len(row.find_all("td")) - 1:
                td.find("a")
                if td.find("a") is not None:
                    link = td.find("a")["href"]
        row_main[principal_header_title[0]] = {secondary_header_title[i]: row_list[i] for i in range(0,4)}
        row_main[principal_header_title[1]] = {secondary_header_title[i]: row_list[i] for i in range(4,8)}
        row_main[principal_header_title[2]] = {secondary_header_title[i]: row_list[i] for i in range(8,15)}
        row_main[principal_header_title[5]] = {secondary_header_title[i]: row_list[i] for i in range(15,20)}
        row_main[principal_header_title[4]] = {secondary_header_title[i]: row_list[i] for i in range(20,24)}
        row_main[principal_header_title[3]] = {secondary_header_title[i]: row_list[i] for i in range(24,29)}
        row_main[row_list[len(row_list) - 1]] = link
        tableau_1.append(row_main)
       
    data_stats = h2.text + ", \n" + str(tableau_1) 
    print(data_stats)


    ######### SECOND TABLEAU #########

    calendar_div = content.find("div", id="all_matchlogs")
    h2 = calendar_div.find("h2")
    table = calendar_div.find("table")
    header = table.select("thead tr")
    th = header[0].find_all("th")
    header_list = []
    for th in th:
       header_list.append(th.text)

    tr = table.select("tbody tr:not(.thead)")
    tableau_2 = []

    for i, tr in enumerate(tr):
        th = tr.find("th")     
        td = tr.find_all("td")
        row_main = {}
        row_main[header_list[0]] = th.text
        td_len = len(td)
        for j, td in enumerate(td):
            if j == td_len - 2:
                row_main[header_list[j+1]] = td.find("a")["href"] if td.find("a") is not None else td.text
            else:
                row_main[header_list[j + 1]] = td.text
        tableau_2.append(row_main)

    data_calendar = h2.text + ", \n" + str(tableau_2)
    print(data_calendar)


    ######### TROISIEME TABLEAU #########

    goal_shoot = content.find("div", id="all_stats_shooting")
    h2 = goal_shoot.find("h2")
    table = goal_shoot.find("table")
    first_header_row = table.find("tr", class_="over_header")
    second_header_row = first_header_row.find_next_sibling("tr")

    first_header_row = first_header_row.find_all("th")
    second_header_row = second_header_row.find_all("th")

    principal_header_title = []
    secondary_header_title = []
   
    for i, header in enumerate(second_header_row):
        secondary_header_title.append(header.text)
   
    for i, header in enumerate(first_header_row):
        principal_header_title.append(header.text)
       
    principal_header_title = [x for x in principal_header_title if x]

    tableau_3 = []
    tr = table.select("tbody tr:not(.thead)")

    for i, row in enumerate(tr):
        row_main = {}
        row_list = []
        th = row.find("th")
        row_list.append(th.text)
        for j, td in enumerate(row.find_all("td")):
            row_list.append(td.text)
            if j == len(row.find_all("td")) - 1:
                td.find("a")
                if td.find("a") is not None:
                    link = td.find("a")["href"]
        row_main = {secondary_header_title[i]: row_list[i] for i in range(0,5)}
        row_main[principal_header_title[0]] = {secondary_header_title[i]: row_list[i] for i in range(5,17)}
        row_main[principal_header_title[1]] = {secondary_header_title[i]: row_list[i] for i in range(17,22)}
        row_main[row_list[len(row_list) - 1]] = link
        tableau_3.append(row_main)
    data_goal_shoot = h2.text + ", \n" + str(tableau_3)
    print(data_goal_shoot)

    '''
    with open("data_stats.json", "w") as f:
        json.dump(tableau_1, f)
        f.close()
    with open("data_calendar.json", "w") as f:
        json.dump(tableau_2, f)
        f.close()
    with open("data_goal_shoot.json", "w") as f:
        json.dump(tableau_3, f)
        f.close()
    '''

else:
    print("Error: " + str(page.status_code))
