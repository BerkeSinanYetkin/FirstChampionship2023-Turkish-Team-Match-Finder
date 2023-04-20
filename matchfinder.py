import requests
import json
import datetime

s = requests.Session()

headers = {
    'X-TBA-Auth-Key': "6TrpiMPEfHhohAkJq1VEW92jtl80byoeDlM9csmdZZEjUQGpQ1Vyl7yA1P5lhE4q"
}

api_request_str_default = "https://www.thebluealliance.com/api/v3"

res = s.get(api_request_str_default + "/event/2023new/teams/simple", headers=headers)

turkish_teams = {}
turkish_teams_div = {
    "2023new": [],
    "2023arc": [],
    "2023cur": [],
    "2023dal": [],
    "2023gal": [],
    "2023hop": [],
    "2023joh": [],
    "2023mil": []
}
turkish_teams_matches = []

divs = {
    "Newton": "2023new",
    "Archimedes": "2023arc",
    "Curie": "2023cur",
    "Daly": "2023dal",
    "Galileo": "2023gal",
    "Hopper": "2023hop",
    "Johnson": "2023joh",
    "Milstein": "2023mil"
}
divs_inverse = {}

def fetch_all_turkish_teams():

    for div in divs.values():
        res = s.get(f"{api_request_str_default}/event/{div}/teams/simple", headers=headers)
        
        for team in range(len(res.json())):
            team_number = res.json()[team]["team_number"]
            team_country = res.json()[team]["country"]
            if team_country == "Turkey":
                turkish_teams[team_number] = res.json()[team]
                turkish_teams_div[div].append(team_number)
    
    print(turkish_teams.keys())
    print(turkish_teams_div)

def fetch_turkish_teams_matches():
    
    for team_number in turkish_teams.keys():

        for div in turkish_teams_div.keys():

            if (turkish_teams_div[div].count(team_number)) == 1:

                number_of_matches = len(s.get(f"{api_request_str_default}/team/frc{team_number}/event/{div}/matches", headers=headers).json())

                for i in range(number_of_matches):
                    data = []
                    data.append(s.get(f"{api_request_str_default}/team/frc{team_number}/event/{div}/matches", headers=headers).json()[i])
                    data.append(team_number)

                    turkish_teams_matches.append(data)

def return_predicted_time(match):
    return match[0]["predicted_time"]

fetch_all_turkish_teams()
fetch_turkish_teams_matches()

turkish_teams_matches.sort(key=return_predicted_time)

for x, y in divs.items():
    divs_inverse.setdefault(y, []).append(x)


for match in turkish_teams_matches:
    predicted_time_cvt = datetime.datetime.fromtimestamp(match[0]["predicted_time"]).strftime("%d/%m/%Y, %H:%M:%S")
    team_number = match[1]
    div = divs_inverse[match[0]["event_key"]]
    match_number = match[0]["match_number"]
    print(team_number, predicted_time_cvt, div, f"{match_number}. Sıralama maçı", sep="-")