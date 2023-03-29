import win32com.client as win32
import os
import pandas as pd
import time
from pathlib import Path
from xiteit import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
from inputimeout import inputimeout

# pip install pypiwin32

MAIL_END = "If you need any further assistance, please open a case through our support channel: https://support.radware.com/app/ask\n\n*DO NOT REPLY TO THIS EMAIL*"
CONTACTS = 'ERT-NOC@radware.com; *ENTER CONTACTS*'
script_path = str(Path(__file__, '..').resolve())
script_path = script_path + "\\"

while True:
    
    userInput = input()
    alerts_info = getAlerts(getToken())

    def whichAlert(userInput):
        for i in alerts_info:
            if i["subject"]==userInput:
                return i


    def BGP_START(alert_info):
        asset = alert_info["value"]
        network = json.loads(alert_info['custom_fields'])["network"].replace(",","")
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = CONTACTS
        mail.Subject = f'BGP Advertising started'
        mail.Body = f"*DO NOT REPLY TO THIS EMAIL*\n\nDear Customer,\n\n During our proactive monitoring, our systems detected that one of your assets started advertising towards Radware cloud. \nDetails:\nAsset: {asset}\nNetwork: {network}\n\n*Paste looking glass screenshot here*\n\n{MAIL_END}"
        mail.display()

    def vipdown(alert_info):
        domain = alert_info["service"]
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = CONTACTS
        mail.Subject = f'Origin down for app - {domain}'
        mail.Body = f"*DO NOT REPLY TO THIS EMAIL*\n\nDear Customer,\n\nDuring our proactive monitoring, our systems detected that one of your applications origin is currently down:\nDomain: {domain}\n\n{MAIL_END}"
        mail.display()

    def gre(alert_info):
        account = json.loads(alert_info['custom_fields'])["account"]
        site = json.loads(alert_info['custom_fields'])["site"]
        peer = json.loads(alert_info['custom_fields'])["internalip"]
        source = json.loads(alert_info['custom_fields'])["sourceip"]
        destination = json.loads(alert_info['custom_fields'])["destinationip"]
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = CONTACTS
        mail.Subject = f'GRE tunnels flap/down'
        mail.Body = f"*DO NOT REPLY TO THIS EMAIL*\n\nDear Customer,\n\nOur monitoring system has detected that the following GRE tunnel(s) is/are currently [down/flapped].\n\nAccount: {account}\nSite: {site}\nTunnel: {peer}\nSource IP: {source}\nDestination IP: {destination}\n\nWe have included a trace of the tunnel(s):\n[Copy the traceroute]\n\n{MAIL_END}"
        mail.display()

    check = whichAlert(userInput)

    if check["severity"] == "GRE+OnCloud":
        gre(check)
    