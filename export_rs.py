# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 13:18:12 2022

@author: arda.ercan
"""

from suds.client import Client # version 0.6 // pip install suds-jurko==0.6
import ssl
from datetime import date, datetime, timedelta
import pytz # version 2021.1 // pip install pytz==2021.1
import pandas as pd # version 1.3.2 // pip install pandas==1.3.2
from tabulate import tabulate # version 0.8.9 // pip install tabulate==0.8.9
import os.path
import os, glob

'''
### Spalten für den Export ###
Wind Speed (avg) = 1002
Rotor Speed [rpm] (avg) = 1005
Active Power (avg) = 1008
Nacelle Position (avg) = 1011
Wind Direction (avg) = 
Generator Speed [rpm] (avg) = 1013
T Outside Nacelle Level (avg) = 1017
Pitch Angle 1 (avg) = 1040

Relative Humidity (avg) = 1218
Air Pressure = 1149
# Riffgat besitzt kein WD Wert
Wind Direction (avg) = 1012
'''

'''
### Merkur ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
Generator Speed
T Outside Nacelle Level
Pitch Angle 1

### Merkur Galileo ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
T Outside Nacelle
Pitch Angle 1

### TWB II ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
Generator Speed
T Outside Nacelle
Pitch Angle 1

### Alpha Ventus Senvion ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
Generator Speed
T Outside Nacelle
Pitch Angle 1

### Alpha Ventus Adwen ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
Generator Speed
T Outside Nacelle
Pitch Angle 1

### Alpha Ventus Adwen 2 ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position
Wind Direction
Generator Speed
T Outside Nacelle
Pitch Angle 1

### Riffgat ###
Wind Speed
Rotor Speed
Active Power
Nacelle Position

Wind Direction fehlt

Generator Speed
T Outside Nacelle
Pitch Angle 1
'''

ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 600)
pd.set_option('display.width', 1200)

# User und Passwort
user = "SOAP"
password = "hkSbWXEU"

# festlegen des Zeitfensters
utc = pytz.UTC
date_start = datetime(2021, 1, 1, 00, 00, 00)
date_end = datetime(2021, 4, 30, 00, 00, 00)
date_start = utc.localize(date_start)
date_end = utc.localize(date_end)


client = Client("https://rotorsoft.omexom-offshore.de/soap/v2/?wsdl", username = user, password = password)
# print(client)

# endP = client.service.getAllEndPoints()
# for f in endP:
#     print(f)



# getAllParks(xs:string userName, xs:string password)
# Gibt die Identifier der Anlagen-Typen zurück
all_parks = client.service.getAllParks(user, password)
print(all_parks)

# getAllPowerUnitDetails(xs:string userName, xs:string password)
# power_unit_det = client.service.getAllPowerUnitDetails(user, password)
# print(power_unit_det)

# getAllPowerUnits(xs:string userName, xs:string password)
# power_units = client.service.getAllPowerUnits(user, password)
# print(power_units)

rawData = Client("https://rotorsoft.omexom-offshore.de/soap/v2/rawdata/?wsdl", username = user, password = password)

rawDataPU = rawData.service.getRawDataForPowerUnits(user, password, 'se600214', date_start, date_end, '10m', '1002')