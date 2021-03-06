# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:13:26 2022

@author: arda.ercan
"""

# Lambda-Funktionen


import pandas as pd
from tkinter import *
import tkinter as tk
#from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from datetime import datetime
import os.path
import math
from tqdm import tqdm
#import plotly.express as px
#import plotly.io as pio

#from filtered_data_bin_averaging_3 import export_df
# pio.renderers.default = "browser"

# import gui_kennl 
# gk = gui_kennl

# from gui_kennl import button_id
# bi = button_id


pd.set_option('display.max_rows', 2000)
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

export_data = False

#TWB II
rotor_diameter = 152
hub_height = 106
ref_air_den = 1.225
rel_hum = 50

#Riffgat
# rotor_diameter = 120
# hub_height = 90

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


weibull_a = 9.59122292031186
weibull_b = 2
#v_mittel = weibull_a * math.exp(GAMMALN(1+1/B8))

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


# User w??hlt CSV Datei aus; Die CSV-wird als DateFrame eingelesen
filename = askopenfile(title="W??hlen Sie eine CSV-Datei aus", filetype=[("csv file", "*.csv")])
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
    
# Datentypen der Spalten werden ge??ndert
for c in df.columns:
    if (c != 'Identifier') and (c != 'DateTime'):
        DataConversion(df, c)

# F??gt Zeit zum DateTime hinzu und wird danach gel??scht
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
    B2: Nabenh??he

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
    
    air_pressure = 1013.25 - 0.12 * hub_height
    return air_pressure


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
    '''
                a = 1 / (f + 273.15)
                b = air_pres(hub_height) * 100 / 287.05
                c = 50 / 100
                d = (0.0631846 * (f + 273.15))
                e = 1 / 287.05
                f = 1 / 461.5
                val = (a * b) - ((c * (0.0000205 ** d)) * (e - f))
                '''

    counter = 0
    for f in tqdm(df['T Outside Nacelle Level']):
        try:
            if f != 0:
                val = 1 / (f + 273.15) * (air_pres(hub_height) * 100 / 287.05 - 50 / 100 * 0.0000205 *
                                          math.exp(0.0631846 * (f + 273.15)) * ((1 / 287.05) - (1 / 461.5)))

                x = f + 273.15
                a = 1000.53 * 100 / 287.05
                b = 50 / 100 * 0.0000205 * math.exp(0.0631846 * x)                           
    	        
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
                value = f * (((df.at[counter, 'Air Density'] / ref_air_den) ** (1/3)))
                df.at[counter, 'Corrected Wind Speed'] = value
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
                value = (df.at[counter, 'Active Power'] * 1000) / (0.5 * df.at[counter, 'Air Density']
                                                             * math.pi * ((rotor_diameter / 2) ** 2) * (df.at[counter, 'Wind Speed'] ** 3))
                df.at[counter, 'Power Coefficient'] = value
            else:
                df.at[counter, 'Power Coefficient'] = 0
        except:
            continue
        counter += 1
    print("Power Coefficient done")

# pd.mask #

# Filter ob Werte ??ber der Untergrenze
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
            if f != 0.00:
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
        if f != 0.0000:
            if act_pow_filter:
                if df.at[counter, 'Active Power'] >= kw1 and df.at[counter, 'Active Power'] <= kw2 and df.at[counter, 'Pitch Angle'] >= (((pit_a2 - pit_a1) / (kw2 - kw1)) * (df.at[counter, 'Active Power'] - kw1)) + pit_a1:
                    df.at[counter, 'Active Power Filter'] = False
                    # print("1. IF")
                    
                if df.at[counter, 'Active Power'] > kw2 and df.at[counter, 'Active Power'] <= kw3 and df.at[counter, 'Pitch Angle'] >= pit_a2:
                    df.at[counter, 'Active Power Filter'] = False
                    # print("2. IF")
                    
                if df.at[counter, 'Active Power'] > kw3 and df.at[counter, 'Active Power'] <= kw4 and df.at[counter, 'Pitch Angle'] >= (((pit_a4 - pit_a3) / (kw4 - kw3)) * (df.at[counter, 'Active Power'] - kw3)) + pit_a3:
                    df.at[counter, 'Active Power Filter'] = False
                    # print("3. IF")
                    
                else:
                    df.at[counter, 'Active Power Filter'] = True
                    # print("1. ELSE")
            else:
                df.at[counter, 'Active Power Filter'] = True
                # print("2. ELSE")
        else:
            df.at[counter, 'Active Power Filter'] = False
        counter += 1


def pitch_angle_filtero():
    global df
    counter = 0
    m = (pit_a2 - pit_a1) / (kw2 - kw1)
    b = 5

    m2 = (pit_a4 - pit_a3) / (kw4 - kw3)
    b2 = -14.3846


    # Alle Active Power Werte unter 1000; Alle Pitch Angle Werte unter 5
    first_section = df[(df['Active Power'] <= kw2) & (df['Pitch Angle'] <= pit_a1)]
    
    # Alle Werte, wo Pitch Angle kleiner gleich Berechnung
    first_section = first_section[((first_section['Active Power'] * m) + b) >= first_section['Pitch Angle']]
    first_section.loc['Active Power Filter'] = True
    #print(first_section)

    second_section = df[(df['Active Power'] > kw2) & (df['Active Power'] <= kw3) & (df['Pitch Angle'] < pit_a3)]
    second_section.loc['Active Power Filter'] = True
    #print("SECOND SECTION")
    #print(second_section)

    third_section = df[(df['Active Power'] > kw3) & (df['Active Power'] <= kw4) & (df['Pitch Angle'] <= pit_a4)]
    third_section = third_section[((third_section['Active Power'] * m2) + b2) >= third_section['Pitch Angle']]
    third_section.loc['Active Power Filter'] = True
    #print("THIRD SECTION")
    #print(third_section)

    fourth_section = df[df['Active Power'] > kw4]
    fourth_section.loc['Active Power Filter'] = True
    

    #df = pd.merge(second_section['Active Power Filter'],first_section['Active Power Filter'], on='Active Power Filter', how='left')

    #df = pd.merge(df, first_section, on='Index', left_index=True, right_index=True)
    #df = pd.join(first_section, on='Identifier')
    #print(df)
    
    #df['Active Power Filter'] = first_section['Active Power Filter']
    #print(df['Active Power Filter'])
    #df['Active Power Filter'] = second_section['Active Power Filter']#, third_section['Active Power Filter'], fourth_section['Active Power Filter']
    #print(df['Active Power Filter'])
    #print("FOURTH SECTION")
    #print(fourth_section)
    for index in df.index:
        if index in first_section.index:
            df.at[counter, 'Active Power Filter'] = True
            #print("IF First Section")
        elif index in second_section.index:
            df.at[counter, 'Active Power Filter'] = True
            #print("ELIF Second Section")
        elif index in third_section.index:
            df.at[counter, 'Active Power Filter'] = True
            #print("ELIF Third Section")
        elif index in fourth_section.index:
            df.at[counter, 'Active Power Filter'] = True
            #print("ELIF Fourth Section")
        else:
            df.at[counter, 'Active Power Filter'] = False
            #print("ELSE")
        counter+=1
    #print(df)

def pitch_angle_filter():
    '''
    kw1 = 0
    kw2 = 1000
    kw3 = 5000
    kw4 = 6300

    pit_a1 = 5
    pit_a2 = 1
    pit_a3 = 1
    pit_a4 = 5

    y = m * x + b

    m = (pit_a2 - pit_a1) / (kw2 - kw1)
    '''
    #-b= (m*x)/y
    #b = -((m*x)/y)
    #y1 = (-0.004 * x1) + 5

    #x1 = (-250 * y1) + 1250


    #y2 = ((4/1300) * x) + -14.3846

    #x2 = (325 * y) + 4675

    # LAMBDA VERSUCH
    #first = lambda m, b, x = (m * x) + b
    #x = lambda a, b, c : a + b + c
    #print(x(5, 6, 2))
    #abc = df.assign(Percentage = lambda x, m, b: ((m * x['Active Power']) + b))
    #print(Percentage(m, b))
    #print(abc['Percentage'])


    

    

    for pitch_angle in tqdm(df['Pitch Angle']):    
        if pitch_angle != 0.0000:
            if act_pow_filter:
                # Erster Teil sollte soweit fertig sein; Anfang zweiten Teil!
                #df[df.loc['Acitve Power'] <= kw2]
                # x & y einzeln filtern und am ende schauen, wo beide true werte haben

                if df.at[counter, 'Active Power'] <= kw2 and pitch_angle > 0 and pitch_angle <= pit_a1:
                    y = (-0.004 * df.at[counter, 'Active Power']) + 5
                    x = (-250 * pitch_angle) + 1250
                    if df.at[counter, 'Active Power'] <= x and y > 0.0000 and pitch_angle <= y:
                        #print()
                        #print("ID: ", df.at[counter, 'Identifier'])
                        #print("Active Power: ", df.at[counter, 'Active Power'])
                        #print("Pitch Angle: ", pitch_angle)
                        #print("Y-Achse: ", y)
                        #print("X-Achse: ", x)
                        #print()
                        df.at[counter, 'Active Power Filter'] = True
                        #print("1. IF")

                elif df.at[counter, 'Active Power'] > kw2 and df.at[counter, 'Active Power'] <= kw3 and pitch_angle <= pit_a3:
                    df.at[counter, 'Active Power Filter'] = True
                    #print()
                    #print("ID: ", df.at[counter, 'Identifier'])
                    #print("Active Power: ", df.at[counter, 'Active Power'])
                    #print("Pitch Angle: ", pitch_angle)
                    #print()
                    #print("2. IF")



                elif df.at[counter, 'Active Power'] > kw3 and df.at[counter, 'Active Power'] <= kw4 and pitch_angle > pit_a3  and pitch_angle <= pit_a4:
                    #print("Active Power: ", df.at[counter, 'Active Power'])
                    #print("Pitch Winkel: ", pitch_angle)
                    y = ((4/1300) * df.at[counter, 'Active Power']) - 14.38461
                    x = (325 * pitch_angle) + 4675
                    #print("X: ", x)
                    #print("Y: ", y)
                    df.at[counter, 'Active Power Filter'] = True
                    if df.at[counter, 'Active Power'] <= x and y > 0.0000 and pitch_angle <= y:
                        #print()
                        #print("ID: ", df.at[counter, 'Identifier'])
                        #print("Active Power: ", df.at[counter, 'Active Power'])
                        #print("Pitch Angle: ", pitch_angle)
                        #print("Y-Achse: ", y)
                        #print("X-Achse: ", x)
                        #print()
                        df.at[counter, 'Active Power Filter'] = True
                        #print("3. IF")
                
                elif df.at[counter, 'Active Power'] > kw4 and pitch_angle > pit_a4:
                    #print("LETZTER ELIF TEIL!")
                    df.at[counter, 'Active Power Filter'] = True

                else:
                    df.at[counter, 'Active Power Filter'] = False
                    #print("Else")
            else:
                df.at[counter, 'Active Power Filter'] = False
        else:
            df.at[counter, 'Active Power Filter'] = False
            #print("2 Else")
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

    #df['NEW BIN'] = pd.cut(df['Corrected Wind Speed'],
                    # -0.25, 0.25 = 1, 0.25, 0.75 = 2, 0.75, 1.25 = 3,
                    #bins
    #                bins=[-0.25, 0.25, 0.75 ,1.25 , 1.75, 2.25, 2.75, 3.25, 3.75 ,4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25, 8.75, 9.25, 9.75, 10.25, 10.75, 11.25, 11.75, 12.25, 12.75, 13.25, 13.75, 14.25, 14.75, 15.25, 15.75, 16.25, 16.75, 17.25, 17.75, 18.25, 18.75, 19.25, 19.75, 20.25, 20.75, 21.25, 21.75, 22.25, 22.75, 23.25, 23.75, 24.25, 24.75, 25.25, 23.75, 26.25, 26.75, 27.25, 27.75, 28.25, 28.75, 29.25, 29.75, 30.25, 30.75, 31.25, 31.75, 32.25, 32.75, 33.25, 33.75, 34.25, 34.75, 35.25, 35.75, 36.25, 36.75, 37.25, 38.75, 38.25, 38.75, 39.25, 39.75, 40.25, 40.75, 41.25, 41.75, 42.25, 42.75, 43.25, 43.75, 44.25, 44.75, 45.25, 45.75, 46.25, 46.75, 47.25, 47.75, 48.25, 48.75, 49.25, 49.75, 50.25, 50.75],
     #               labels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])
    #print("bin_test BINNING")
    #print(bin_test)

    return df



# Methods to run
# rename_columns(df)
air_density()
cor_wind_speed()
power_coeff()
lower_limit_filter()
pitch_angle_filtero()
#act_pow_curve_filter()
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


# print(pd.cut(df['Corrected Wind Speed'], [0,1,2,3,4,5,6,7,8,9,10], labels='Bin'))


df = df.drop(labels=['DateTime', 'Nacelle Position', 'Wind Direction', 'Generator Speed', 'Wind Speed', 'Power Coefficient'], axis = 1)
print("dropped some Columns!")

df = df.replace({'Identifier' : twb_rename})
print("Identifier changed!")

df = df.sort_values(by=['Identifier', 'Bin'], ascending = True)
df = df.reset_index(drop = True)
print("Dataframe sorted")


#print("BIN 11:")
#print(df[(df['Identifier'] == 'BW 28') & (df['Bin'] == 11)])

#print("BIN 12:")
#print(df[(df['Identifier'] == 'BW 28') & (df['Bin'] == 12)])

#print(df[ (df['Identifier'] == 'BW 28') & (df['Pitch Angle'] == 0.61) & (df['T Outside Nacelle Level'] == 8.07)])

print("BIN 20")
print(df[(df['Bin'] == 20) & (df['Identifier'] == 'BW 08')])

#df = df[(df['Lower Limit Filter'] == True) & (df['Active Power Filter'] == True)]

print(df)

# Exportiert die CSV
if export_data:
    date = datetime.now().strftime("%Y%m%d")
    my_exportFile = "./export/" + date + ".csv"
    exportfile_my = "./export/" + date + "Pisiklet" +".csv"
    vers = 0
    while os.path.isfile(my_exportFile):
        vers = vers + 1
        my_exportFile = "./export/" + date + "(" + str(vers) + ")" + ".csv"
    df[df['Active Power Filter'] == 0.00].to_csv(my_exportFile, sep=';', decimal=',')
    df[df['Lower Limit Filter'] == 0.00].to_csv(exportfile_my, sep=';', decimal=',')
    print("Data exported")

#???