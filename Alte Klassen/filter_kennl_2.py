# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:49:05 2022

@author: arda.ercan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:49:06 2022

@author: arda.ercan
"""


# Lambda-Funktionen
# Dictionary für Renamer
# 


import pandas as pd
from tkinter import *
import tkinter as tk
#import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from datetime import datetime
import os.path
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
import plotly.express as px
import re
import plotly.io as pio
# pio.renderers.default = "browser"

# import gui_kennl 
# gk = gui_kennl

# from gui_kennl import button_id
# bi = button_id


pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 2000)

'''
### Dictionary ###
rd = Rotordurchmesser
hh = Hub Heigth
ref_air_den = Reference Air Density (constant)
rel_hum = Relative Humidity (constant)

lower_limit_filter = Filter
lower_limit_val = Lower Limit (constant)

act_pow_filter = Filter 
kw1 = Actie Power kW (constant)
kw2 = Actie Power kW (constant)
kw3 = Actie Power kW (constant)
kw4 = Actie Power kW (constant)
pit_a1 = Upper Limit Pitch Angle (constant)
pit_a2 = Upper Limit Pitch Angle (constant)
pit_a3 = Upper Limit Pitch Angle (constant)
pit_a4 = Upper Limit Pitch Angle (constant)
'''
rd = 152
hh = 106
ref_air_den = 1.225
rel_hum = 50


# Lower Limit Rotor Speed Filter
lower_limit_filter = True
# Lower Limit der Turbine
lower_limit_val = 6.4

# Curtailment Curve Filter Werte
# Active Power Filter
act_pow_filter = True
# Active Power [kW] Values
kw1 = 0
kw2 = 1000
kw3 = 5000
kw4 = 6300


# Upper Limit Pitch Angle
pit_a1 = 5
pit_a2 = 1
pit_a3 = 1
pit_a4 = 5

# Variables for the Pitch Plot
xpitch_plt = [kw1, kw2, kw3, kw4]
ypitch_plt = [pit_a1, pit_a2, pit_a3, pit_a4]

# Varibable for the RPM Plot
xrpm_plt = [-1000, 7000]
yrpm_plt = [lower_limit_val, lower_limit_val]


begin = datetime.now()
print("start tool: ", begin)


def DataConversion(df, column):
    '''
    This function correct and convert a column in a data set to make it
    usable as string.

    It first remove the points of thousand in the german synthax,
    it then replace the comas by dot
    and finally convert it as float

    Parameters
    ----------
    data : DataFrame
        Use the data set
    column : TYPE
        Name of the column to convert in float in the data set

    Returns
    -------
    None.

    '''
    try:
        df[column] = df[column].str.replace('.', '', regex = True)
        df[column] = df[column].str.replace(',', '.', regex = True)
        df[column] = df[column].astype(float)
        # print(column,'corrected')
    except:
        print(column, 'not corrected')


# User wählt CSV Datei aus; Die CSV-wird als DateFrame eingelesen
filename = askopenfile(title="Wählen Sie eine CSV-Datei aus", filetype=[("csv file", "*.csv")])
df = pd.read_csv(filename, sep=';', skiprows=None)


# Umbennen der Spaltennamen
# def rename_columns(df):
df = df.rename(columns={'Datum (Anlage)': 'DateTime'})
df = df.rename(columns={'Identifier (Anlage)': 'Identifier'})
df = df.rename(columns={'Wind Speed (avg)': 'Wind Speed'})
df = df.rename(columns={'Rotor Speed [rpm] (avg)': 'Rotor Speed'})
df = df.rename(columns={'Active Power (avg)': 'Active Power'})
df = df.rename(columns={'Nacelle Position (avg)': 'Nacelle Position'})
df = df.rename(columns={'Wind Direction (avg)': 'Wind Direction'})
df = df.rename(columns={'Generator Speed [rpm] (avg)': 'Generator Speed'})
df = df.rename(columns={'T Outside Nacelle Level (avg)': 'T Outside Nacelle Level'})
df = df.rename(columns={'Pitch Angle 1 (avg)': 'Pitch Angle'})
    # df['DateTime'] = pd.to_datetime(df['DateTime'] + ' ' + df['Zeit (Anlage)'])
    # df = df.drop(['Zeit (Anlage)'], axis=1)


# Datentypen der Spalten werden geändert
for c in df.columns:
    if (c != 'Identifier') and (c != 'DateTime'):
        DataConversion(df, c)

# Fügt Zeit zum DateTime hinzu und wird danach gelöscht
df['DateTime'] = pd.to_datetime(df['DateTime'] + ' ' + df['Zeit (Anlage)'])
df = df.drop(['Zeit (Anlage)'], axis=1)




def rename_mrkID(df):
    counter = 0
    for turbines in df.iterrows():
        if df.at[counter, 'Identifier'] == 'GE60178795':
            df.at[counter, 'Identifier'] = 'MO 01'
        if df.at[counter, 'Identifier'] == 'GE60178796':
            df.at[counter, 'Identifier'] = 'MO 02'
        if df.at[counter, 'Identifier'] == 'GE60178797':
            df.at[counter, 'Identifier'] = 'MO 03'
        if df.at[counter, 'Identifier'] == 'GE60178798':
            df.at[counter, 'Identifier'] = 'MO 04'
        if df.at[counter, 'Identifier'] == 'GE60178799':
            df.at[counter, 'Identifier'] = 'MO 05'
        if df.at[counter, 'Identifier'] == 'GE60178800':
            df.at[counter, 'Identifier'] = 'MO 06'
        if df.at[counter, 'Identifier'] == 'GE60178801':
            df.at[counter, 'Identifier'] = 'MO 07'
        if df.at[counter, 'Identifier'] == 'GE60178802':
            df.at[counter, 'Identifier'] = 'MO 08'
        if df.at[counter, 'Identifier'] == 'GE60178803':
            df.at[counter, 'Identifier'] = 'MO 09'
        if df.at[counter, 'Identifier'] == 'GE60178804':
            df.at[counter, 'Identifier'] = 'MO 10'
        if df.at[counter, 'Identifier'] == 'GE60178805':
            df.at[counter, 'Identifier'] = 'MO 12'
        if df.at[counter, 'Identifier'] == 'GE60178806':
            df.at[counter, 'Identifier'] = 'MO 13'
        if df.at[counter, 'Identifier'] == 'GE60178807':
            df.at[counter, 'Identifier'] = 'MO 14'            
        if df.at[counter, 'Identifier'] == 'GE60178808':
            df.at[counter, 'Identifier'] = 'MO 15'
        if df.at[counter, 'Identifier'] == 'GE60178809':
            df.at[counter, 'Identifier'] = 'MO 16'
        if df.at[counter, 'Identifier'] == 'GE60178810':
            df.at[counter, 'Identifier'] = 'MO 17'
        if df.at[counter, 'Identifier'] == 'GE60178811':
            df.at[counter, 'Identifier'] = 'MO 18'
        if df.at[counter, 'Identifier'] == 'GE60178812':
            df.at[counter, 'Identifier'] = 'MO 19'
        if df.at[counter, 'Identifier'] == 'GE60178813':
            df.at[counter, 'Identifier'] = 'MO 20'            
        if df.at[counter, 'Identifier'] == 'GE60178814':
            df.at[counter, 'Identifier'] = 'MO 21'
        if df.at[counter, 'Identifier'] == 'GE60178815':
            df.at[counter, 'Identifier'] = 'MO 22'
        if df.at[counter, 'Identifier'] == 'GE60178816':
            df.at[counter, 'Identifier'] = 'MO 23'
        if df.at[counter, 'Identifier'] == 'GE60178817':
            df.at[counter, 'Identifier'] = 'MO 24'
        if df.at[counter, 'Identifier'] == 'GE60178818':
            df.at[counter, 'Identifier'] = 'MO 25'
        if df.at[counter, 'Identifier'] == 'GE60178819':
            df.at[counter, 'Identifier'] = 'MO 26'     
        if df.at[counter, 'Identifier'] == 'GE60178820':
            df.at[counter, 'Identifier'] = 'MO 27'
        if df.at[counter, 'Identifier'] == 'GE60178821':
            df.at[counter, 'Identifier'] = 'MO 28'
        if df.at[counter, 'Identifier'] == 'GE60178822':
            df.at[counter, 'Identifier'] = 'MO 29'
        if df.at[counter, 'Identifier'] == 'GE60178823':
            df.at[counter, 'Identifier'] = 'MO 30'
        if df.at[counter, 'Identifier'] == 'GE60178824':
            df.at[counter, 'Identifier'] = 'MO 31'
        if df.at[counter, 'Identifier'] == 'GE60178825':
            df.at[counter, 'Identifier'] = 'MO 32'
        if df.at[counter, 'Identifier'] == 'GE60178826':
            df.at[counter, 'Identifier'] = 'MO 33'
        if df.at[counter, 'Identifier'] == 'GE60178827':
            df.at[counter, 'Identifier'] = 'MO 34'
        if df.at[counter, 'Identifier'] == 'GE60178828':
            df.at[counter, 'Identifier'] = 'MO 35'
        if df.at[counter, 'Identifier'] == 'GE60178829':
            df.at[counter, 'Identifier'] = 'MO 36'
        if df.at[counter, 'Identifier'] == 'GE60178831':
            df.at[counter, 'Identifier'] = 'MO 37'
        if df.at[counter, 'Identifier'] == 'GE60178832':
            df.at[counter, 'Identifier'] = 'MO 38'
        if df.at[counter, 'Identifier'] == 'GE60178833':
            df.at[counter, 'Identifier'] = 'MO 39'
        if df.at[counter, 'Identifier'] == 'GE60178834':
            df.at[counter, 'Identifier'] = 'MO 40'
        if df.at[counter, 'Identifier'] == 'GE60178835':
            df.at[counter, 'Identifier'] = 'MO 41'
        if df.at[counter, 'Identifier'] == 'GE60178836':
            df.at[counter, 'Identifier'] = 'MO 42'
        if df.at[counter, 'Identifier'] == 'GE60178837':
            df.at[counter, 'Identifier'] = 'MO 43'
        if df.at[counter, 'Identifier'] == 'GE60178838':
            df.at[counter, 'Identifier'] = 'MO 44'
        if df.at[counter, 'Identifier'] == 'GE60178839':
            df.at[counter, 'Identifier'] = 'MO 45'
        if df.at[counter, 'Identifier'] == 'GE60178840':
            df.at[counter, 'Identifier'] = 'MO 46'
        if df.at[counter, 'Identifier'] == 'GE60178841':
            df.at[counter, 'Identifier'] = 'MO 47'
        if df.at[counter, 'Identifier'] == 'GE60178842':
            df.at[counter, 'Identifier'] = 'MO 48'
        if df.at[counter, 'Identifier'] == 'GE60178843':
            df.at[counter, 'Identifier'] = 'MO 49'
        if df.at[counter, 'Identifier'] == 'GE60178844':
            df.at[counter, 'Identifier'] = 'MO 50'
        if df.at[counter, 'Identifier'] == 'GE60178845':
            df.at[counter, 'Identifier'] = 'MO 51'
        if df.at[counter, 'Identifier'] == 'GE60178846':
            df.at[counter, 'Identifier'] = 'MO 52'
        if df.at[counter, 'Identifier'] == 'GE60178847':
            df.at[counter, 'Identifier'] = 'MO 53'
        if df.at[counter, 'Identifier'] == 'GE60178848':
            df.at[counter, 'Identifier'] = 'MO 54'
        if df.at[counter, 'Identifier'] == 'GE60178849':
            df.at[counter, 'Identifier'] = 'MO 55'
        if df.at[counter, 'Identifier'] == 'GE60178850':
            df.at[counter, 'Identifier'] = 'MO 56'
        if df.at[counter, 'Identifier'] == 'GE60178851':
            df.at[counter, 'Identifier'] = 'MO 57'
        if df.at[counter, 'Identifier'] == 'GE60178852':
            df.at[counter, 'Identifier'] = 'MO 58'
        if df.at[counter, 'Identifier'] == 'GE60178853':
            df.at[counter, 'Identifier'] = 'MO 59'
        if df.at[counter, 'Identifier'] == 'GE60178854':
            df.at[counter, 'Identifier'] = 'MO 60'
        if df.at[counter, 'Identifier'] == 'GE60178855':
            df.at[counter, 'Identifier'] = 'MO 61'
        if df.at[counter, 'Identifier'] == 'GE60178856':
            df.at[counter, 'Identifier'] = 'MO 62'
        if df.at[counter, 'Identifier'] == 'GE60178857':
            df.at[counter, 'Identifier'] = 'MO 63'
        if df.at[counter, 'Identifier'] == 'GE60178858':
            df.at[counter, 'Identifier'] = 'MO 64'
        if df.at[counter, 'Identifier'] == 'GE60178859':
            df.at[counter, 'Identifier'] = 'MO 65'
        if df.at[counter, 'Identifier'] == 'GE60178860':
            df.at[counter, 'Identifier'] = 'MO 66'
        counter += 1
# Dictionary 
def rename_twbID(df):
    counter = 0
    for turbines in df.iterrows():
        if df.at[counter, 'Identifier'] == 'se600214':
            df.at[counter, 'Identifier'] = 'BW 05'
        if df.at[counter, 'Identifier'] == 'bw06':
            df.at[counter, 'Identifier'] = 'BW 06'
        if df.at[counter, 'Identifier'] == 'se600216':
            df.at[counter, 'Identifier'] = 'BW 07'
        if df.at[counter, 'Identifier'] == 'bw08':
            df.at[counter, 'Identifier'] = 'BW 08'
        if df.at[counter, 'Identifier'] == 'bw09':
            df.at[counter, 'Identifier'] = 'BW 09'
        if df.at[counter, 'Identifier'] == 'bw10':
            df.at[counter, 'Identifier'] = 'BW 10'
        if df.at[counter, 'Identifier'] == 'bw11':
            df.at[counter, 'Identifier'] = 'BW 11'
        if df.at[counter, 'Identifier'] == 'se600213':
            df.at[counter, 'Identifier'] = 'BW 16'
        if df.at[counter, 'Identifier'] == 'bw17':
            df.at[counter, 'Identifier'] = 'BW 17'
        if df.at[counter, 'Identifier'] == 'bw18':
            df.at[counter, 'Identifier'] = 'BW 18'
        if df.at[counter, 'Identifier'] == 'bw19':
            df.at[counter, 'Identifier'] = 'BW 19'
        if df.at[counter, 'Identifier'] == 'bw20':
            df.at[counter, 'Identifier'] = 'BW 20'
        if df.at[counter, 'Identifier'] == 'bw27':
            df.at[counter, 'Identifier'] = 'BW 27'
        if df.at[counter, 'Identifier'] == 'bw28':
            df.at[counter, 'Identifier'] = 'BW 28'
        if df.at[counter, 'Identifier'] == 'bw29':
            df.at[counter, 'Identifier'] = 'BW 29'
        if df.at[counter, 'Identifier'] == 'bw30':
            df.at[counter, 'Identifier'] = 'BW 30'
        if df.at[counter, 'Identifier'] == 'bw45':
            df.at[counter, 'Identifier'] = 'BW 45'
        if df.at[counter, 'Identifier'] == 'bw56':
            df.at[counter, 'Identifier'] = 'BW 56'
        if df.at[counter, 'Identifier'] == 'bw57':
            df.at[counter, 'Identifier'] = 'BW 57'
        if df.at[counter, 'Identifier'] == 'bw59':
            df.at[counter, 'Identifier'] = 'BW 59'
        if df.at[counter, 'Identifier'] == 'bw60':
            df.at[counter, 'Identifier'] = 'BW 60'
        if df.at[counter, 'Identifier'] == 'bw67':
            df.at[counter, 'Identifier'] = 'BW 67'
        if df.at[counter, 'Identifier'] == 'bw68':
            df.at[counter, 'Identifier'] = 'BW 68'
        if df.at[counter, 'Identifier'] == 'bw70':
            df.at[counter, 'Identifier'] = 'BW 70'
        if df.at[counter, 'Identifier'] == 'bw71':
            df.at[counter, 'Identifier'] = 'BW 71'
        if df.at[counter, 'Identifier'] == 'bw72':
            df.at[counter, 'Identifier'] = 'BW 72'
        if df.at[counter, 'Identifier'] == 'bw73':
            df.at[counter, 'Identifier'] = 'BW 73'
        if df.at[counter, 'Identifier'] == 'bw74':
            df.at[counter, 'Identifier'] = 'BW 74'
        if df.at[counter, 'Identifier'] == 'bw75':
            df.at[counter, 'Identifier'] = 'BW 75'
        if df.at[counter, 'Identifier'] == 'bw76':
            df.at[counter, 'Identifier'] = 'BW 76'
        if df.at[counter, 'Identifier'] == 'bw77':
            df.at[counter, 'Identifier'] = 'BW 77'
        if df.at[counter, 'Identifier'] == 'bw78':
            df.at[counter, 'Identifier'] = 'BW 78'
        if df.at[counter, 'Identifier'] == 'se980445':
            df.at[counter, 'Identifier'] = 'PMU'
        counter += 1

def rename_avsID(df):
    counter = 0
    for turbines in df.iterrows():
        if df.at[counter, 'Identifier'] == 're120018':
            df.at[counter, 'Identifier'] = 'AV 01'
        if df.at[counter, 'Identifier'] == 're120019':
            df.at[counter, 'Identifier'] = 'AV 02'
        if df.at[counter, 'Identifier'] == 're120020':
            df.at[counter, 'Identifier'] = 'AV 03'
        if df.at[counter, 'Identifier'] == 're120021':
            df.at[counter, 'Identifier'] = 'AV 04'
        if df.at[counter, 'Identifier'] == 're120022':
            df.at[counter, 'Identifier'] = 'AV 05'
        if df.at[counter, 'Identifier'] == 're120023':
            df.at[counter, 'Identifier'] = 'AV 06'
        counter += 1
        
def rename_avaID(df):
    counter = 0
    for turbines in df.iterrows():
        if df.at[counter, 'Identifier'] == 'arv000010':
            df.at[counter, 'Identifier'] = 'AV 07'
        if df.at[counter, 'Identifier'] == 'arv00009':
            df.at[counter, 'Identifier'] = 'AV 08'
        if df.at[counter, 'Identifier'] == 'arv000008':
            df.at[counter, 'Identifier'] = 'AV 09'
        if df.at[counter, 'Identifier'] == 'arv00007':
            df.at[counter, 'Identifier'] = 'AV 10'
        if df.at[counter, 'Identifier'] == 'arv00006':
            df.at[counter, 'Identifier'] = 'AV 11'
        if df.at[counter, 'Identifier'] == 'arv00005':
            df.at[counter, 'Identifier'] = 'AV 12'
        counter += 1

def rename_rgID(df):
    counter = 0
    for turbines in df.iterrows():
        if df.at[counter, 'Identifier'] == 'swt3601268':
            df.at[counter, 'Identifier'] = 'R01'
        if df.at[counter, 'Identifier'] == 'swt3601269':
            df.at[counter, 'Identifier'] = 'R02'
        if df.at[counter, 'Identifier'] == 'swt3601270':
            df.at[counter, 'Identifier'] = 'R03'
        if df.at[counter, 'Identifier'] == 'swt3601271':
            df.at[counter, 'Identifier'] = 'R04'
        if df.at[counter, 'Identifier'] == 'swt3601272':
            df.at[counter, 'Identifier'] = 'R05'
        if df.at[counter, 'Identifier'] == 'swt3601273':
            df.at[counter, 'Identifier'] = 'R06'
        if df.at[counter, 'Identifier'] == 'swt3601274':
            df.at[counter, 'Identifier'] = 'R07'
        if df.at[counter, 'Identifier'] == 'swt3601275':
            df.at[counter, 'Identifier'] = 'R08'
        if df.at[counter, 'Identifier'] == 'swt3601276':
            df.at[counter, 'Identifier'] = 'R09'
        if df.at[counter, 'Identifier'] == 'swt3601277':
            df.at[counter, 'Identifier'] = 'R10'
        if df.at[counter, 'Identifier'] == 'swt3601278':
            df.at[counter, 'Identifier'] = 'R11'
        if df.at[counter, 'Identifier'] == 'swt3601279':
            df.at[counter, 'Identifier'] = 'R12'
        if df.at[counter, 'Identifier'] == 'swt3601280':
            df.at[counter, 'Identifier'] = 'R13'
        if df.at[counter, 'Identifier'] == 'swt3601281':
            df.at[counter, 'Identifier'] = 'R14'
        if df.at[counter, 'Identifier'] == 'swt3601282':
            df.at[counter, 'Identifier'] = 'R15'
        if df.at[counter, 'Identifier'] == 'swt3601283':
            df.at[counter, 'Identifier'] = 'R16'
        if df.at[counter, 'Identifier'] == 'swt3601284':
            df.at[counter, 'Identifier'] = 'R17'
        if df.at[counter, 'Identifier'] == 'swt3601285':
            df.at[counter, 'Identifier'] = 'R18'
        if df.at[counter, 'Identifier'] == 'swt3601286':
            df.at[counter, 'Identifier'] = 'R19'
        if df.at[counter, 'Identifier'] == 'swt3601287':
            df.at[counter, 'Identifier'] = 'R20'
        if df.at[counter, 'Identifier'] == 'swt3601288':
            df.at[counter, 'Identifier'] = 'R21'
        if df.at[counter, 'Identifier'] == 'swt3601289':
            df.at[counter, 'Identifier'] = 'R22'
        if df.at[counter, 'Identifier'] == 'swt3601290':
            df.at[counter, 'Identifier'] = 'R23'
        if df.at[counter, 'Identifier'] == 'swt3601291':
            df.at[counter, 'Identifier'] = 'R24'
        if df.at[counter, 'Identifier'] == 'swt3601292':
            df.at[counter, 'Identifier'] = 'R25'
        if df.at[counter, 'Identifier'] == 'swt3601293':
            df.at[counter, 'Identifier'] = 'R26'
        if df.at[counter, 'Identifier'] == 'swt3601294':
            df.at[counter, 'Identifier'] = 'R27'
        if df.at[counter, 'Identifier'] == 'swt3601295':
            df.at[counter, 'Identifier'] = 'R28'
        if df.at[counter, 'Identifier'] == 'swt3601296':
            df.at[counter, 'Identifier'] = 'R29'
        if df.at[counter, 'Identifier'] == 'swt3601297':
            df.at[counter, 'Identifier'] = 'R30'  
        counter += 1



# #df['Wind Speed'] = df['Wind Speed'].astype(float)
# df['Rotor Speed'] = df['Rotor Speed'].astype(float)
# df['Active Power'] = df['Active Power'].astype(float)
# df['Nacelle Position'] = df['Nacelle Position'].astype(float)
# df['Wind Direction'] = df['Wind Direction'].astype(float)


# print(df['Wind Speed'])
# for f in df['Wind Speed']:
# if f > 10:
print(df)
# Input + Filter Seite

# Hier wird der Luftdruck berechnet


def air_pres(hh):
    '''
    ### Air Pressure ###
    B2: Nabenhöhe

    =1013,25-0,12*$B$2

    Parameters
    ----------
    hh : TYPE
        DESCRIPTION.

    Returns
    -------
    air_p : TYPE
        DESCRIPTION.

    '''
    
    air_p = 1013.25 - 0.12 * hh
    return air_p


# Hier wird die relative Luftfeuchtigkeit berechnet

def rel_humidity():
    print()


# Hier wird die Luftdichtekorrektur berechnet
def air_density():
    '''
    ### Air Density  ### nach [IEC 61400-12-1, eq. 12] Standard
    I = T Outside Nacelle Level (avg)
    K = Air Pressure
    L = Relative Humidity

    =WENN(I13 <> ""  ;  1 / (I13 + 273,15) * (K13 * 100 / 287,05 - L13 / 100 * 0,0000205 * EXP(0,0631846 * (I13 + 273,15)) * (1 / 287,05 - 1 / 461,5)) ; "")
                               1 / 280,59 * (25,83261480626057)
    Returns
    -------
    None.

    '''
    co = 0
    for f in tqdm(df['T Outside Nacelle Level']):
        try:
            if f != 0:
                val = 1 / (f + 273.15) * (air_pres(hh) * 100 / 287.05 - 50 / 100 * 0.0000205 *
                                          math.exp(0.0631846 * (f + 273.15)) * ((1 / 287.05) - (1 / 461.5)))
                df.at[co, 'Air Density'] = val
            else:
                df.at[co, 'Air Density'] = 0
        except:
            continue
        co += 1
    print("Air Density done")

# Hier wird die korregierte Windgeschwindigkeit berechnet


def cor_wind_speed():
    '''
    ### Density Corrected Wind Speed  ### [IEC 61400-12-1, eq. 14]
    C = Wind Speed (avg)
    M = Air Density
    B4 = Reference Air Density (constant)

    =WENN(C13 <> ""  ;  C13 * (M13 / $B$4) ^ (1 / 3)  ;  "")

    if c13 != 0:
        C13 * (M13 / $B$4) ^ (1 / 3)

    Returns
    -------
    None.

    '''
    co = 0
    for f in tqdm(df['Wind Speed']):
        try:   
            if f != 0:
                val = f * (((df.at[co, 'Air Density'] / ref_air_den) ** (1/3)))
                df.at[co, 'Corrected Wind Speed'] = val
            else:
                df.at[co, 'Corrected Wind Speed'] = 0
        except:
            continue
        co += 1
    print("Corrected Wind Speed done")

# Hier wird die Power Coefficiente berechnet
def power_coeff():
    '''
    ### Power Coefficient ### [IEC 61400-12-1, eq. 20]
    C = Wind Speed (avg)
    E = Active Power (avg)
    B1 = Rotordurchmesser (constant)
    M = Air Density

    =WENN(C13 <> ""  ;  E13 * 1000 / (0,5 * M13 * PI() * ($B$1 / 2) ^ 2 * C13 ^ 3)  ;  "")
    if c13 != 0:
        E13 * 1000 / (0,5 * M13 * PI() * ($B$1 / 2) ^ 2 * C13 ^ 3)
    Returns
    -------
    None.

    '''

    co = 0
    for f in tqdm(df['Wind Speed']):
        try:
            if f != 0:
                val = (df.at[co, 'Active Power'] * 1000) / (0.5 * df.at[co, 'Air Density']
                                                             * math.pi * ((rd / 2) ** 2) * (df.at[co, 'Wind Speed'] ** 3))
                df.at[co, 'Power Coefficient'] = val
            else:
                df.at[co, 'Power Coefficient'] = 0
        except:
            continue
        co += 1
    print("Power Coefficient done")


# Filter ob Werte über der Untergrenze
def lower_limit_filter():
    '''
    ### Lower Limit Rotor Speed Filter ###
    D13 = Rotor Speed
    S10 = Boolean (Ob Filter an oder aus)
    S6 = 6,4 (Filter Value)


    =WENN(D13="";"";
          WENN($S$10="";1;
               WENN(D13>=$S$6;1;0)
               )
          )

    Returns
    -------
    None.

    '''
    counter = 0
    for f in tqdm(df['Rotor Speed']):
        try:
            if f != 0:
                if lower_limit_filter:
                    if f >= lower_limit_val:
                        df.at[counter, 'Lower Limit Filter'] = True
                    else:
                        df.at[counter, 'Lower Limit Filter'] = False
                else:
                    df.at[counter, 'Lower Limit Filter'] = True
            else:
                df.at[counter, 'Lower Limit Filter'] = False
        except:
            continue
        counter += 1
    print("Lower Limit Filter used!")


def act_pow_curve_filter():
    '''
    J = Pitch Angle (avg)
    T10 = Filter (non-)active
    E = Active Power (avg)
    T6 = 0 - Active Power (constant)
    T7 = 1000 - Acitve Power (constant)
    T8 = 5000 - Active Power (constant)
    T9 = 6300 - Active Power (constant)
    U6 = 5 - Upper Limit Pitch Angle (constant)
    U7 = 1 - Upper Limit Pitch Angle (constant)
    U8 = 1 - Upper Limit Pitch Angle (constant)
    U9 = 5 - Upper Limit Pitch Angle (constant)

    =WENN(J13 = ""  ;  ""  ;  
          WENN($T$10 = ""  ;  1  ;  
               WENN(ODER
                    (UND(E13 >= $T$6  ;  E13 <= $T$7  ;  J13 >= ($U$7 - $U$6) / ($T$7 - $T$6) * (E13 - $T$6) + $U$6)  ;  
                     UND(E13 > $T$7  ;  E13 <= $T$8  ;  J13 >= $U$7)  ;  
                     UND(E13 > $T$8  ;  E13 <= $T$9  ;  J13 >= ($U$9 - $U$8) / ($T$9 - $T$8) * (E13 - $T$8) + $U$8)
                     )
                    ;  0  ;  1)
               )
          )



    Alte Formel:
    (pit_a2 - pit_a1) / (((kw2 - kw1) * (df.at[counter, 'Active Power'] - kw1)) + pit_a1)
    
    Neue Formel:
    (((pit_a2 - pit_a1) / (kw2 - kw1)) * (df.at[counter, 'Active Power'] - kw1)) + pit_a1
    
    Returns
    -------
    None.
    '''
    print("Active Power Filter start!")
    counter = 0
    for f in tqdm(df['Pitch Angle']):    
        if f != '':
            if act_pow_filter:
                try:
                    if df.at[counter, 'Active Power'] >= kw1 and df.at[counter, 'Active Power'] <= kw2 and df.at[counter, 'Pitch Angle'] >= ((pit_a2 - pit_a1) / (kw2 - kw1) * (df.at[counter, 'Active Power'] - kw1)) + pit_a1:
                        df.at[counter, 'Active Power Filter'] = False
                        # print("1. IF")
                        
                    elif df.at[counter, 'Active Power'] > kw2 and df.at[counter, 'Active Power'] <= kw3 and df.at[counter, 'Pitch Angle'] >= pit_a2:
                        df.at[counter, 'Active Power Filter'] = False
                        # print("2. IF")
                        
                    elif df.at[counter, 'Active Power'] > kw3 and df.at[counter, 'Active Power'] <= kw4 and df.at[counter, 'Pitch Angle'] >= ((pit_a4 - pit_a3) / (kw4 - kw3) * (df.at[counter, 'Active Power'] - kw3)) + pit_a3:
                        df.at[counter, 'Active Power Filter'] = False
                        # print("3. IF")
                        
                    else:
                        df.at[counter, 'Active Power Filter'] = True
                        # print("1. ELSE")
                except:
                    continue
            else:
                df.at[counter, 'Active Power Filter'] = True
                # print("2. ELSE")
                
        else:
            df.at[counter, 'Active Power Filter'] = False


def df_bin(df):
    '''
    N = Density Corrected Wind Speed

    =WENN(N13="";"";2+GANZZAHL((N13-0,25)/0,5))

    Returns
    -------
    None.
    '''
    print("start df_bin")
    counter = 0
    for f in tqdm(df['Corrected Wind Speed']):
        if f != 0:
            try:
                val = 2 + int((f - 0.25) / 0.5)
                df.at[counter, 'Bin'] = val
            except:
                df.at[counter, 'Bin'] = 0
        counter += 1
    print("df_bin end")
    return df


def pitch_plot(df):
    '''
    Returns
    -------
    None.
    '''
    # size of the plot
    plt.figure(figsize = (15, 15))
    
    # Range of the Plot
    plt.xlim([0, 7000])
    plt.ylim([0, 25])
    
    df_filt = df[(df['Lower Limit Filter'] == True) & (df['Active Power Filter'] == True)]
    
    # Setting of the Name (Plotname, x- & y-axisname)
    plt.title("Pitch Diagram")
    plt.xlabel("elektrische Leistungsabgabe (kW)")
    plt.ylabel("Pitchwinkel")

    plt.plot(xpitch_plt, ypitch_plt, color = 'red')
    plt.scatter(df_filt['Active Power'], df_filt['Pitch Angle'], color = 'blue')
    
   
    
    plt.minorticks_on()
    plt.grid(b = True, which = 'both')
    plt.show()
    plt.savefig('pitch.png')
    print('Pitch Plot ploted')
    return df

def rpm_plot(df):
    '''
    Returns
    -------
    None.
    '''
    plt.figure(figsize = (20, 20))
    
    plt.xlim([-1000, 7000])
    plt.ylim([0, 12])
    
    df_filt = df[(df['Lower Limit Filter'] == True)]
     
    plt.title("RPM Diagram")
    plt.xlabel("elektrische Leistungsabgabe (kW)")
    plt.ylabel("Rotordrehzahl [1/min]")
    
   
    
    plt.plot(xrpm_plt, yrpm_plt, color = 'red')
    plt.scatter(df_filt['Active Power'], df_filt['Rotor Speed'], color = 'blue')
    
    plt.minorticks_on()
    plt.grid()
    plt.show()
    plt.savefig('rpm.png')
    print("RPM Plot ploted")
    return df
    

def plotly_express_test(df):
    
    df_filter = px.data.iris()
    df_filter = df
    df_filter = df[(df['Lower Limit Filter'] == True) & (df['Active Power Filter'] == True)]
    
    baro = px.bar(df_filter['Active Power'], df_filter['Rotor Speed'])
    baro.show()
    print("baro Plot ploted")
    return df



def renamer(df, buttonID):
    if buttonID == 1:
        rename_mrkID(df)
    elif buttonID == 2:
        rename_twbID(df)
    elif buttonID == 3:
        rename_avsID(df)
    elif buttonID == 4:
        rename_avaID(df)
    elif buttonID == 5:
        rename_rgID(df)
        

# Methods to run
# rename_columns(df)
air_density()
cor_wind_speed()
power_coeff()
lower_limit_filter()
df_bin(df)
rename_twbID(df)
# renamer(df, bi)
df = df.sort_values(by=['Bin'], ascending = True)
df = df.reset_index(drop = True)
act_pow_curve_filter()
pitch_plot(df)
rpm_plot(df)
# plotly_express_test(df)


df = df.drop(labels=['DateTime', 'Nacelle Position', 'Wind Direction', 'Generator Speed'], axis = 1)

print(df)

# Exportiert die CSV
date = datetime.now().strftime("%Y%m%d")
my_exportFile = "./export/" + date + ".csv"
vers = 0
while os.path.isfile(my_exportFile):
    vers = vers + 1
    my_exportFile = "./export/" + date + "(" + str(vers) + ")" + ".csv"
df.to_csv(my_exportFile, sep=';', decimal=',')
print("Data exported")

#↓