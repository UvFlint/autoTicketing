import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import urllib3

dotenv_path = Path(r'C:\Users\YuvalMo\OneDrive - Radware LTD\Desktop\Scripts\GitlabRepo\yuvalm-scripts\.env')
load_dotenv(dotenv_path=dotenv_path)

XITEIT_USER = os.getenv("XITEIT_USER") 
XITEIT_PASSWORD = os.getenv("XITEIT_PASSWORD")

def getToken():

    url = "https://api.xiteit.co/api-auth-user/?format=json"

    payload = {
        "username" : XITEIT_USER,
        "password" : XITEIT_PASSWORD
    }

    r = requests.post(url, data=payload, verify = False)
    r = r.json()
    token = r["token"]
    return token

def getAlerts(token):

    header = {
        'Content-Type': 'application/json',
        'Authorization' : "Token "+token
    }

    alertsURL = "https://api.xiteit.co/api/alerts/get/?format=json&customer=108&group_by=host&groups_and_kpis=-1&noteboard=false&nowork=false&open_alerts={}&order_by=default&page=1&request_key=1670027183668&searched=&show_recovered=true&wanted=active"

    r = requests.get(alertsURL, headers=header, verify=False)
    r = r.json()
    r = r["data"]
    return r

