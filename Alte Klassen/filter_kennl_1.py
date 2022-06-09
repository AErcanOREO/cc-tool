# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:49:06 2022

@author: arda.ercan
"""
import pandas as pd
from tkinter import *
import tkinter as tk
#import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import math
import matplotlib.pyplot as plt

#from gui_kennl import *

pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 600)
pd.set_option('display.width', 1600)

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
xpitch_plot = [kw1, kw2, kw3, kw4]
ypitch_plot = [pit_a1, pit_a2, pit_a3, pit_a4]



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
        df[column] = df[column].str.replace('.', '')
        df[column] = df[column].str.replace(',', '.')
        df[column] = df[column].astype(float)
        # print(column,'corrected')
    except:
        print(column, 'not corrected')


# User wählt CSV Datei aus; Die CSV-wird als DateFrame eingelesen
filename = askopenfile(title="Wählen Sie eine CSV-Datei aus",
                       filetype=[("csv file", "*.csv")])
df = pd.read_csv(filename, sep=';', skiprows=None)


# Umbennen der Spaltennamen
df = df.rename(columns={'Datum (Anlage)': 'DateTime'})
df = df.rename(columns={'Identifier (Anlage)': 'Identifier'})
df = df.rename(columns={'Wind Speed (avg)': 'Wind Speed'})
df = df.rename(columns={'Rotor Speed [rpm] (avg)': 'Rotor Speed'})
df = df.rename(columns={'Active Power (avg)': 'Active Power'})
df = df.rename(columns={'Nacelle Position (avg)': 'Nacelle Position'})
df = df.rename(columns={'Wind Direction (avg)': 'Wind Direction'})
df = df.rename(columns={'Generator Speed [rpm] (avg)': 'Generator Speed'})
df = df.rename(
    columns={'T Outside Nacelle Level (avg)': 'T Outside Nacelle Level'})
df = df.rename(columns={'Pitch Angle 1 (avg)': 'Pitch Angle'})


# Datentypen der Spalten werden geändert
for c in df.columns:
    if (c != 'Identifier') and (c != 'DateTime'):
        DataConversion(df, c)


# Fügt Zeit zum DateTime hinzu und wird danach gelöscht
df['DateTime'] = pd.to_datetime(df['DateTime'] + ' ' + df['Zeit (Anlage)'])
df = df.drop(['Zeit (Anlage)'], axis=1)

# #df['Wind Speed'] = df['Wind Speed'].astype(float)
# df['Rotor Speed'] = df['Rotor Speed'].astype(float)
# df['Active Power'] = df['Active Power'].astype(float)
# df['Nacelle Position'] = df['Nacelle Position'].astype(float)
# df['Wind Direction'] = df['Wind Direction'].astype(float)


print(df)

# print(df['Wind Speed'])
# for f in df['Wind Speed']:
# if f > 10:
# print(f)
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
    for f in df['T Outside Nacelle Level']:
        if f != 0:
            val = 1 / (f + 273.15) * (air_pres(hh) * 100 / 287.05 - 50 / 100 * 0.0000205 *
                                      math.exp(0.0631846 * (f + 273.15)) * ((1 / 287.05) - (1 / 461.5)))
            df.loc[co, 'Air Density'] = val
        else:
            df.loc[co, 'Air Density'] = 0
        co += 1

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
    for f in df['Wind Speed']:
        if f != 0:
            val = f * (((df.loc[co, 'Air Density'] / ref_air_den) ** (1/3)))
            df.loc[co, 'Corrected Wind Speed'] = val
        else:
            df.loc[co, 'Corrected Wind Speed'] = 0
        co += 1


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
    for f in df['Wind Speed']:
        if f != 0:
            val = (df.loc[co, 'Active Power'] * 1000) / (0.5 * df.loc[co, 'Air Density']
                                                         * math.pi * ((rd / 2) ** 2) * (df.loc[co, 'Wind Speed'] ** 3))
            df.loc[co, 'Power Coefficient'] = val
        else:
            df.loc[co, 'Power Coefficient'] = 0
        co += 1


# Filter ob Werte über der Untergrenze
def lower_limit_filter():
    '''
    ### Lower Limit Rotor Speed Filter ###
    D13 = Rotor Speed
    S10 = Boolean (Ob Filter an oder aus)
    S6 = 6,4 (Filter Value)


    =WENN(D13="";"";WENN($S$10="";1;WENN(D13>=$S$6;1;0)))

    Returns
    -------
    None.

    '''
    co = 0
    for f in df['Rotor Speed']:
        if f != 0:
            if lower_limit_filter:
                if f >= lower_limit_val:
                    df.loc[co, 'Lower Limit Filter'] = True

                else:
                    df.loc[co, 'Lower Limit Filter'] = False
            else:
                df.loc[co, 'Lower Limit Filter'] = False
        else:
            df.loc[co, 'Lower Limit Filter'] = False
        co += 1


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
                     )  ;  0  ;  1)))

    =WENN(J13="";"";WENN($T$10="";1;WENN(ODER(UND(E13>=$T$6;E13<=$T$7;J13>=($U$7-$U$6)/($T$7-$T$6)*(E13-$T$6)+$U$6);UND(E13>$T$7;E13<=$T$8;J13>=$U$7);UND(E13>$T$8;E13<=$T$9;J13>=($U$9-$U$8)/($T$9-$T$8)*(E13-$T$8)+$U$8));0;1)))

    Returns
    -------
    None.

    '''
    co = 0
    for f in df['Pitch Angle']:
        if f != 0:
            if act_pow_filter:
                if df.loc[co, 'Active Power'] >= kw1 and df.loc[co, 'Active Power'] <= kw2 and df.loc[co, 'Pitch Angle'] >= (pit_a2 - pit_a1) / (((kw2 - kw1) * (df.loc[co, 'Active Power'] - kw1)) + kw1):
                    df.loc[co, 'Active Power Filter'] = False
                elif df.loc[co, 'Active Power'] > kw2 and df.loc[co, 'Active Power'] <= kw3 and df.loc[co, 'Pitch Angle'] >= pit_a2:
                    df.loc[co, 'Active Power Filter'] = False
                elif df.loc[co, 'Active Power'] > kw3 and df.loc[co, 'Active Power'] <= kw4 and df.loc[co, 'Pitch Angle'] >= (pit_a4 - pit_a3) / (((kw4 - kw3) * (df.loc[co, 'Active Power'] - kw2)) + pit_a2):
                    df.loc[co, 'Active Power Filter'] = False
                else:
                    df.loc[co, 'Active Power Filter'] = True

            else:
                df.loc[co, 'Active Power Filter'] = True
        else:
            df.loc[co, 'Active Power Filter'] = False
        co += 1


def df_bin():
    '''
    N = Density Corrected Wind Speed

    =WENN(N13="";"";2+GANZZAHL((N13-0,25)/0,5))

    Returns
    -------
    None.
    '''
    co = 0
    for f in df['Corrected Wind Speed']:
        if f != 0:
            val = 2 + int((f - 0.25) / 0.5)
            df.loc[co, 'Bin'] = val
        else:
            df.loc[co, 'Bin'] = 0
        co += 1


def PlotData(df):
    '''
    
    Returns
    -------
    None.
    '''
    plt.figure(figsize = (15, 15))
    df_filt = df[(df['Lower Limit Filter'] == True) & (df['Active Power Filter'] == True)]
    
    # #data_filt = data[(data['Positiv Filter']==False) & (data['Stuck Filter']== False) & (data['Standard Filter']== False) ]
    # #data_filt_advanced = data[(data['Positiv Filter']==False) & (data['Stuck Filter']== False) & (data['Standard Filter']== False) & (data['Reversed Standard Filter']== False) & (data['Median Curve Filter']== False) & (data['Reversed Median Curve Filter']== False)]
    # if not 'Rectangle Filter' in data.columns:
    #     data_filt_final = data[(data['Positiv Filter'] == False) & (data['Stuck Filter'] == False) & (data['Median Curve Filter'] == False) & (data['Reversed Median Curve Filter'] == False)]
    # else:
    #     data_filt_final = data[(data['Positiv Filter'] == False) & (data['Stuck Filter'] == False) & (data['Median Curve Filter'] == False) & (data['Reversed Median Curve Filter'] == False) & (data['Rectangle Filter'] == False)]
    # data_filt_positive = data[(data['Positiv Filter'] == True)]
    # data_filt_advanced = data[(data['Positiv Filter'] == False) & (data['Stuck Filter'] == False) & (data['Median Curve Filter'] == False) & (data['Reversed Median Curve Filter'] == False)]
    
    plt.title("Pitch Diagram")
    plt.xlabel("elektrische Leistungsabgabe (kW")
    plt.ylabel("Pitchwinkel")

    
    # plt.axis([0, 7000, 0, 25])
    # plt.plot(df['Active Power'], df['Pitch Angle'], color = 'blue')
    plt.plot(xpitch_plot, ypitch_plot, color = 'red')
    plt.scatter(df_filt['Active Power'], df_filt['Pitch Angle'], color = 'blue')
    
    
    
    # plt.plot(data_filt_advanced['Wind Speed (avg)'], data_filt_advanced['Active Power (avg)'],'r.')
    # plt.plot(data_filt_positive['Wind Speed (avg)'], data_filt_positive['Active Power (avg)'],'g.')
    # plt.plot(data_filt_final['Corrected Windspeed'], data_filt_final['Active Power (avg)'],'c.')
    
    plt.xlim([0, 7000])
    plt.ylim([0, 25])
    
    plt.minorticks_on()
    plt.grid(b = True, which = 'both')
    print('Scheme ploted')
    plt.show()

air_density()
cor_wind_speed()
power_coeff()
lower_limit_filter()
act_pow_curve_filter()
df_bin()
PlotData(df)


# df = df.drop(labels=['DateTime'], axis = 1)

print(df)
# print()
# print("Lower Limit Limit = 1: \n", df.iloc[3864])
# print()
# print("Active Power Filter = 1: \n", df.iloc[3865])
# print()
# print("Beide Filter = 0: \n", df.iloc[3866])
# print()





#↓