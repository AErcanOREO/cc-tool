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
rotor_diameter = Rotordurchmesser
hub_height = Hub Heigth
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

#TWB II
# rotor_diameter = 152
# hub_height = 106
ref_air_den = 1.225
rel_hum = 50

#Riffgat
rotor_diameter = 120
hub_height = 90

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

if 'Wind Direction (avg)' not in df.columns:
    df['Wind Direction (avg'] = None
    print("Column 'Wind Direction (avg)' added")
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



mrk_rename = { 'GE60178795': 'MO 01',
                'GE60178796': 'MO 02',
                'GE60178797': 'MO 03',
                'GE60178798': 'MO 04',
                'GE60178799': 'MO 05',
                'GE60178800': 'MO 06',
                'GE60178801': 'MO 07',
                'GE60178802': 'MO 08',
                'GE60178803': 'MO 09',
                'GE60178804': 'MO 10',
                'GE60178805': 'MO 12',
                'GE60178806': 'MO 13',
                'GE60178807': 'MO 14',            
                'GE60178808': 'MO 15',
                'GE60178809': 'MO 16',
                'GE60178810': 'MO 17',
                'GE60178811': 'MO 18',
                'GE60178812': 'MO 19',
                'GE60178813': 'MO 20',            
                'GE60178814': 'MO 21',
                'GE60178815': 'MO 22',
                'GE60178816': 'MO 23',
                'GE60178817': 'MO 24',
                'GE60178818': 'MO 25',
                'GE60178819': 'MO 26',     
                'GE60178820': 'MO 27',
                'GE60178821': 'MO 28',
                'GE60178822': 'MO 29',
                'GE60178823': 'MO 30',
                'GE60178824': 'MO 31',
                'GE60178825': 'MO 32',
                'GE60178826': 'MO 33',
                'GE60178827': 'MO 34',
                'GE60178828': 'MO 35',
                'GE60178829': 'MO 36',
                'GE60178831': 'MO 37',
                'GE60178832': 'MO 38',
                'GE60178833': 'MO 39',
                'GE60178834': 'MO 40',
                'GE60178835': 'MO 41',
                'GE60178836': 'MO 42',
                'GE60178837': 'MO 43',
                'GE60178838': 'MO 44',
                'GE60178839': 'MO 45',
                'GE60178840': 'MO 46',
                'GE60178841': 'MO 47',
                'GE60178842': 'MO 48',
                'GE60178843': 'MO 49',
                'GE60178844': 'MO 50',
                'GE60178845': 'MO 51',
                'GE60178846': 'MO 52',
                'GE60178847': 'MO 53',
                'GE60178848': 'MO 54',
                'GE60178849': 'MO 55',
                'GE60178850': 'MO 56',
                'GE60178851': 'MO 57',
                'GE60178852': 'MO 58',
                'GE60178853': 'MO 59',
                'GE60178854': 'MO 60',
                'GE60178855': 'MO 61',
                'GE60178856': 'MO 62',
                'GE60178857': 'MO 63',
                'GE60178858': 'MO 64',
                'GE60178859': 'MO 65',
                'GE60178860': 'MO 66' }

twb_rename = {'se600214': 'BW 05',
                'bw06': 'BW 06',
                'se600216': 'BW 07',
                'bw08': 'BW 08',
                'bw09': 'BW 09',
                'bw10': 'BW 10',
                'bw11': 'BW 11',
                'se600213': 'BW 16',
                'bw17': 'BW 17',
                'bw18': 'BW 18',
                'bw19': 'BW 19',
                'bw20': 'BW 20',
                'bw27': 'BW 27',
                'bw28': 'BW 28',
                'bw29': 'BW 29',
                'bw30': 'BW 30',
                'bw45': 'BW 45',
                'bw56': 'BW 56',
                'bw57': 'BW 57',
                'bw59': 'BW 59',
                'bw60': 'BW 60',
                'bw67':'BW 67',
                'bw68': 'BW 68',
                'bw70': 'BW 70',
                'bw71': 'BW 71',
                'bw72': 'BW 72',
                'bw73': 'BW 73',
                'bw74': 'BW 74',
                'bw75': 'BW 75',
                'bw76': 'BW 76',
                'bw77': 'BW 77',
                'bw78': 'BW 78',
                'se980445': 'PMU' }

# Alte Variante die Identifier zu ändern


avs_rename = { 're120018':'AV 01',
                're120019': 'AV 02',
                're120020': 'AV 03',
                're120021': 'AV 04',
                're120022': 'AV 05',
                're120023': 'AV 06'}
        
ava_rename = { 'arv000010': 'AV 07',
                'arv00009': 'AV 08',
                'arv000008': 'AV 09',
                'arv00007': 'AV 10',
                'arv00006': 'AV 11',
                'arv00005': 'AV 12' }

rg_rename = { 'swt3601268': 'R01',
                'swt3601269': 'R02',
                'swt3601270': 'R03',
                'swt3601271': 'R04',
                'swt3601272': 'R05',
                'swt3601273': 'R06',
                'swt3601274': 'R07',
                'swt3601275': 'R08',
                'swt3601276': 'R09',
                'swt3601277': 'R10',
                'swt3601278': 'R11',
                'swt3601279': 'R12',
                'swt3601280': 'R13',
                'swt3601281': 'R14',
                'swt3601282': 'R15',
                'swt3601283': 'R16',
                'swt3601284': 'R17',
                'swt3601285': 'R18',
                'swt3601286': 'R19',
                'swt3601287': 'R20',
                'swt3601288': 'R21',
                'swt3601289': 'R22',
                'swt3601290': 'R23',
                'swt3601291': 'R24',
                'swt3601292': 'R25',
                'swt3601293': 'R26',
                'swt3601294': 'R27',
                'swt3601295': 'R28',
                'swt3601296': 'R29',
                'swt3601297': 'R30'  }




# #df['Wind Speed'] = df['Wind Speed'].astype(float)
# df['Rotor Speed'] = df['Rotor Speed'].astype(float)
# df['Active Power'] = df['Active Power'].astype(float)
# df['Nacelle Position'] = df['Nacelle Position'].astype(float)
# df['Wind Direction'] = df['Wind Direction'].astype(float)


# print(df['Wind Speed'])
# for f in df['Wind Speed']:
# if f > 10:
# Input + Filter Seite

# Hier wird der Luftdruck berechnet


def air_pres(hub_height):
    '''
    ### Air Pressure ###
    B2: Nabenhöhe

    =1013,25-0,12*$B$2

    Parameters
    ----------
    hub_height : TYPE
        DESCRIPTION.

    Returns
    -------
    air_p : TYPE
        DESCRIPTION.

    '''
    
    air_p = 1013.25 - 0.12 * hub_height
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
    counter = 0
    for f in tqdm(df['T Outside Nacelle Level']):
        try:
            if f != 0:
                val = 1 / (f + 273.15) * (air_pres(hub_height) * 100 / 287.05 - 50 / 100 * 0.0000205 *
                                          math.exp(0.0631846 * (f + 273.15)) * ((1 / 287.05) - (1 / 461.5)))
                df.at[counter, 'Air Density'] = val
            else:
                df.at[counter, 'Air Density'] = 0
        except:
            continue
        counter += 1
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
    counter = 0
    for f in tqdm(df['Wind Speed']):
        try:   
            if f != 0:
                val = f * (((df.at[counter, 'Air Density'] / ref_air_den) ** (1/3)))
                df.at[counter, 'Corrected Wind Speed'] = val
            else:
                df.at[counter, 'Corrected Wind Speed'] = 0
        except:
            continue
        counter += 1
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

    counter = 0
    for f in tqdm(df['Wind Speed']):
        try:
            if f != 0:
                val = (df.at[counter, 'Active Power'] * 1000) / (0.5 * df.at[counter, 'Air Density']
                                                             * math.pi * ((rotor_diameter / 2) ** 2) * (df.at[counter, 'Wind Speed'] ** 3))
                df.at[counter, 'Power Coefficient'] = val
            else:
                df.at[counter, 'Power Coefficient'] = 0
        except:
            continue
        counter += 1
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
        counter += 1


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

# rename_twbID()
# renamer(df, bi)

df = df.sort_values(by=['Bin'], ascending = True)
df = df.reset_index(drop = True)

act_pow_curve_filter()
pitch_plot(df)
rpm_plot(df)
# plotly_express_test(df)


# print(pd.cut(df['Corrected Wind Speed'], [0,1,2,3,4,5,6,7,8,9,10] ,labels=False))


df = df.drop(labels=['DateTime', 'Nacelle Position', 'Wind Direction', 'Generator Speed'], axis = 1)
print("dropped some Columns!")

print("change Identifier")

df = df.replace({'Identifier' : rg_rename})
print("Identifier changed!")

# Exportiert die CSV
date = datetime.now().strftime("%Y%m%d")
my_exportFile = "./export/" + date + ".csv"
vers = 0
while os.path.isfile(my_exportFile):
    vers = vers + 1
    my_exportFile = "./export/" + date + "(" + str(vers) + ")" + ".csv"
df.to_csv(my_exportFile, sep=';', decimal=',')
print("Data exported")

print(df)


#↓



'''
def rename_twbID():
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
'''