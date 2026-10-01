import requests
from requests.structures import CaseInsensitiveDict
import json

from ics import Calendar, Event

#retrieve planning
def get_planning(token, date_debut="2021-03-06", date_fin="2022-05-06"):
  url = f"https://aurion-prod.enac.fr/mobile/mon_planning?date_debut={date_debut}&date_fin={date_fin}"

  headers = CaseInsensitiveDict()
  headers["Host"] = "aurion-prod.enac.fr"
  #headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
  headers["Accept"] = "application/json, text/plain, */*"
  headers["Accept-Language"] = "fr-FR,fr;q=0.9"
  headers["Accept-Encoding"] = "gzip, deflate, br"
  headers["Authorization"] = "Bearer "+ token
  headers["Content-Type"] = "application/json"
  #headers["Origin"] = "http://localhost:8000"
  headers["DNT"] = "1"
  headers["Connection"] = "keep-alive"
  #headers["Referer"] = "http://localhost:8000/"
  headers["Sec-Fetch-Dest"] = "empty"
  headers["Sec-Fetch-Mode"] = "cors"
  headers["Sec-Fetch-Site"] = "cross-site"

  resp = requests.get(url, headers=headers)
  return resp.json()


#connexion :
def get_token(username, password): #return JASON MOMOA

  url = "https://aurion-prod.enac.fr/mobile/login"

  headers = CaseInsensitiveDict()
  headers["Host"] = "aurion-prod.enac.fr"
  #headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
  headers["Accept"] = "application/json, text/plain, */*"
  headers["Accept-Language"] = "fr"
  headers["Accept-Encoding"] = "gzip, deflate, br"
  headers["Content-Type"] = "application/json"
  headers["Content-Length"] = "42"
  #headers["Origin"] = "http://localhost:8000"
  headers["DNT"] = "1"
  headers["Connection"] = "keep-alive"
  #headers["Referer"] = "http://localhost:8000/"
  headers["Sec-Fetch-Dest"] = "empty"
  headers["Sec-Fetch-Mode"] = "cors"
  headers["Sec-Fetch-Site"] = "cross-site"
  headers["Sec-GPC"] = "1"

  body = json.dumps({"login":username,"password":password})
  resp = requests.post(url, headers=headers, data=body)
  if resp.json()["normal"] == None:
    print("erreur de login ou de mdp !")
    return None
  return resp.json()["normal"]

def generate_ics(json):
  c = Calendar()

  for cours in json:
    if cours['id'] != None:
      formatedCours = Event()
      formatedCours.name = cours['favori']['f3'] + " _ " + cours['favori']['f2']
      formatedCours.begin = cours['date_debut'] #TODO check
      formatedCours.end = cours['date_fin'] #TODO check
      formatedCours.uid = str(cours['id']) #TODO check
      formatedCours.description = f"""
         - Matière - Cours :   {cours['favori']['f3']}
        - Intervenant : {cours['favori']['f5']}
        - Salle : {cours['favori']['f3']}

        """
      #print(formatedCours)
      c.events.add(formatedCours)
  return c
