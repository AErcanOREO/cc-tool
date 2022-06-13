from concurrent.futures import process
from suds.client import Client
import ssl
from datetime import date, datetime, timedelta
import pytz
import pandas as pd
import numpy as np
from tabulate import tabulate

ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 600)
pd.set_option('display.width', 1200)

# User und Passwort
user = "SOAP"
password = "hkSbWXEU"

# festlegen des Zeitfensters
utc = pytz.UTC
date_start = datetime(2021, 5, 1, 00, 00, 00)
date_end = datetime(2021, 5, 1, 5, 00, 00)
ten_min = datetime(2021, 5, 1, 00, 10, 00)

date_start = utc.localize(date_start)
date_end = utc.localize(date_end)
ten_min = utc.localize(ten_min)


# Spalten
data = {'Anlage': [],  # 0
            'Id': [],  # 1
            'Startdatum': [],  # 2
            'Vorgangsname': [],  # 3
            'RS Ereignis': [],  # 4
            'Entstörungsanzahl': [],  # 5
            'Entstörungsdauer': [],  # 6
            'Ertragsausfall Ent': [],  # 7
            'Dauer ges': [],  # 8
            'Ertragsverlust ges': [] }  # 9

df = pd.DataFrame(data)

client = Client("https://rotorsoft.omexom-offshore.de/soap/v3/?wsdl", username=user, password=password)

print(client)

allend = client.service.getAllEndPoints()
print(allend)

basic = Client("https://rotorsoft.omexom-offshore.de/soap/v3/basicdata/?wsdl", username=user, password=password)

print(basic)

proces = Client("https://rotorsoft.omexom-offshore.de/soap/v3/process/?wsdl", username = user, password = password)

print(proces)

data_processList = client.service.getAllParks(user, password)
print(data_processList)
#for i in data_processList.processes:
 #   print("I : ", i)