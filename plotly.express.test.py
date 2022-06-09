# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:51:53 2022

@author: arda.ercan
"""
import pandas as pd
from tkinter import *
import tkinter as tk
import plotly.express as px
from tqdm import tqdm
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

lower_limit_val = 6.4
act_pow_filter = True
kw1 = 0
kw2 = 1000
kw3 = 5000
kw4 = 6300


# Upper Limit Pitch Angle
pit_a1 = 5
pit_a2 = 1
pit_a3 = 1
pit_a4 = 5

filename = '../Desktop/Kennlinientool - Bachelor/Raw Data/twb01-14012021 5 Anlagen.csv'
df = pd.read_csv(filename, sep=';', skiprows=None)

def DataConversion(df, column):
    try:
        df[column] = df[column].str.replace('.', '', regex = True)
        df[column] = df[column].str.replace(',', '.', regex = True)
        df[column] = df[column].astype(float)
        # print(column,'corrected')
    except:
        print(column, 'not corrected')

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


# Filter ob Werte über der Untergrenze
def lower_limit_filter():
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
    print("Active Power Curve Filter done!")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="scatter-plot"),
    html.P("Petal Width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=2.5, step=0.1,
        marks={0: '0', 2.5: '2.5'},
        value=[0.5, 2]
    ),
])


lower_limit_filter()
act_pow_curve_filter()

df_filter = df[(df['Lower Limit Filter'] == True) & (df['Active Power Filter'] == True)]
df_filter = px.data.iris()

baro = px.bar(df_filter, df_filter['Active Power'], df_filter['Pitch Angle'])
baro.show()


app.run_server(debug=True)
# df = px.data.gapminder().query("year == 2007")
# px.histogram(df, x = 'lifeExp', marginal = "rug", hover_name="country")