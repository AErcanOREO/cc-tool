# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:13:26 2022

@author: arda.ercan
"""

# Lambda-Funktionen
# Dictionary für Renamer


import pandas as pd
from tkinter import *
import tkinter as tk
#import PyPDF2
#from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from datetime import datetime
import os.path
import math
#import matplotlib.pyplot as plt
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
    df['Wind Direction (avg)'] = None
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


twb_rename = { 'se600214': 'BW 05',
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
        
            counter += 1
    print("Lower Limit Filter used!")

def lower_limit_counter():
    counter = 0
    for i in df['Lower Limit Filter']:
        if i == True:
            df.at[counter, 'Positiv Lower Limit'] = 1
        else:
            df.at[counter, 'Negativ Lower Limit'] = 1
        counter += 1
    df['Positiv Lower Limit'] = df['Positiv Lower Limit'].fillna(0)
    df['Negativ Lower Limit'] = df['Negativ Lower Limit'].fillna(0)

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

def act_pow_counter():
    counter = 0
    for i in df['Active Power Filter']:
        if i == True:
            df.at[counter, 'Positiv Active Power'] = 1
        else:
            df.at[counter, 'Negativ Active Power'] = 1
        counter += 1
    df['Positiv Active Power'] = df['Positiv Active Power'].fillna(0)
    df['Negativ Active Power'] = df['Negativ Active Power'].fillna(0)

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
act_pow_curve_filter()
df_bin(df)

'''
### Lambdaversuch ###
value = map(lambda f: 2 + int((f - 0.25) / 0.5) if f != 0 else 0, df[df['Corrected Wind Speed']])
df ['Bin'] = df['Bin'].append(value(df['Corrected Wind Speed']))
print("value:",value)
print("df", df)
'''


# rename_twbID()
# renamer(df, bi)

# Counter for 
lower_limit_counter()
act_pow_counter()


pitch_plot(df)
rpm_plot(df)
# plotly_express_test(df)


# print(pd.cut(df['Corrected Wind Speed'], [0,1,2,3,4,5,6,7,8,9,10] ,labels=False))


df = df.drop(labels=['DateTime', 'Nacelle Position', 'Wind Direction', 'Generator Speed', 'Wind Speed', 'Power Coefficient'], axis = 1)
print("dropped some Columns!")

df = df.replace({'Identifier' : twb_rename})
print("Identifier changed!")

df = df.sort_values(by=['Identifier', 'Bin'], ascending = True)
df = df.reset_index(drop = True)
print("Dataframe sorted")

print(df)

# Zählt die True und False Einträge
# Speichert Pro Anlage 1 Wert (1 True & 1 False)

def count_true_or_false(column):
    negtest = df.groupby(['Negativ Lower Limit', 'Bin', 'Identifier'], sort=True, as_index=False).size()#.unstack(fill_value=0)
    print("negtest: ", negtest)
    print()
    bintest = df.groupby(['Bin', 'Negativ Lower Limit', 'Identifier'], sort=True, as_index=False).size()#.unstack(fill_value=0)
    print("bintest: ", bintest)
    print()
    idtest = df.groupby(['Identifier', 'Bin', 'Negativ Lower Limit'], sort=True, as_index=False).size()#.unstack(fill_value=0)
    print("idtest: ", idtest)
    print()
    
    neg_low_lim = df.groupby(['Identifier', 'Bin', column], sort=True, as_index=False).size()#.unstack(fill_value=0)
    print(neg_low_lim)
    print(column)
    # for i in df[column]:
    #     print(i)
    
    '''
    Alter Vorgang
    neg_low_lim = df.value_counts((['Identifier', 'Negativ Lower Limit']), sort=True, ascending=True)
    pos_low_lim = df.value_counts((['Identifier', 'Positiv Lower Limit']), sort=True, ascending=True)
    
    neg_act_pow = df.value_counts((['Identifier', 'Negativ Active Power']), sort=True, ascending=True)
    pos_act_pow = df.value_counts((['Identifier', 'Positiv Active Power']), sort=True, ascending=True)
    '''
    counter = 0
    start = 0
    end = 1
    true_val = 0
    false_val = 0
    # amcik = pd.DataFrame(neg_low_lim.tolist())
    # print("amcik: ", amcik)
    # print("neg_low_lim", neg_low_lim)
    # print("pos_low_lim", pos_low_lim)
    # print("neg_act_pow", neg_act_pow)
    # print("pos_act_pow", pos_act_pow)
    
    # print("neg_act_pow[2]:", neg_act_pow[2])
    
    # df['Negativ Lower Limit'] = neg_low_lim 
    # df['Positiv Lower Limit'] = pos_low_lim
    
    # df['Negativ Active Power'] = neg_act_pow
    # df['Positiv Active Power'] = pos_act_pow
    
    # print(df)
    # for i in range(len(neg_low_lim)):
        
    #     # if df.at[counter, 'Bin'] == neg_low_lim('Identifier'):
    #     #     print("if!")
    #     # else:
    #     #     print("else")
    #     print("neg_low_lim[i]: ",neg_low_lim[i])
    #     print("neg_low_lim:", neg_low_lim)
    
    # for i in df['Identifier']:
        # df.at[counter, 'Negativ Lower Limit'] = neg_low_lim[counter]
        # df.at[counter, 'Positiv Lower Limit'] = pos_low_lim[counter]
        
        # df.at[counter, 'Negativ Active Power'] = neg_act_pow[counter]
        # df.at[counter, 'Positiv Active Power'] = pos_act_pow[counter]
        
        # print("i:",i)
        # print("df.at[counter, i]:", df.at[counter, 'Identifier'])
        # print("df.at[counter + 1, i]; ", df.at[counter + 1, 'Identifier'])
        # if df.at[counter, 'Identifier'] != df.at[counter + 1, 'Identifier']:
        #     end = counter
        #     print(df.value_counts((['Identifier', 'Negativ Lower Limit']),sort=True, ascending=True) )
            
        #     ges = end - start
        #     start = counter
        # counter+=1

# count_true_or_false('Negativ Lower Limit')


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


'''
Negativ Lower Limit 
Positiv Lower Limit 
Positiv Active Power 
Negativ Active Power
'''

#↓