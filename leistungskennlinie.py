# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:12:58 2022

@author: arda.ercan
"""

import pandas as pd
from datetime import datetime
import math
import os.path
from tqdm import tqdm

import filter_export as fkpy

fk = fkpy.df

# export = True

data = {'BIN': [],
        'Identifier': [],
        'V': [],
        'P': [],
        'n': [],
        'cp': [],
        'P max': [],
        'P min': [],
        'P std': [],
        'P std/sqrt(n)': []}

df_f = pd.DataFrame(data)

twb_kennlinie = [ {'Identifier': 'HK', 'V': 3, 'P': 0},
                  {'Identifier': 'HK', 'V': 3.5, 'P': 5.112170643 },
                  {'Identifier': 'HK', 'V': 4, 'P': 126.5348803 },
                  {'Identifier': 'HK', 'V': 5, 'P': 457.1223788 },
                  {'Identifier': 'HK', 'V': 6, 'P': 1007.110478 },
                  {'Identifier': 'HK', 'V': 7, 'P': 1743.022208 },
                  {'Identifier': 'HK', 'V': 8, 'P': 2642.228084 },
                  {'Identifier': 'HK', 'V': 9, 'P': 3746.834988 },
                  {'Identifier': 'HK', 'V': 10, 'P': 5092.412141},
                  {'Identifier': 'HK', 'V': 11, 'P': 6245.352513},
                  {'Identifier': 'HK', 'V': 11.5, 'P': 6386.350148},
                  {'Identifier': 'HK', 'V': 12, 'P':  6386.350148},
                  {'Identifier': 'HK', 'V': 13, 'P':  6386.350148},
                  {'Identifier': 'HK', 'V': 14, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 15, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 16, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 17, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 18, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 19, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 20, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 21, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 22, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 23, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 24, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 25, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 26, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 27, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 28, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 29, 'P':   6386.350148},
                  {'Identifier': 'HK', 'V': 30, 'P':   6386.350148}]

'''
rg_kennlinie = [{'Identifier': 'HK', 'V': , 'P': },
                 'Identifier': 'HK', 'V': , 'P': },
                 'Identifier': 'HK', 'V': , 'P': }]
'''

# Werte, die nicht der Filterung entsprechen, werden rausgeworfen aus der Tabelle
fk = fk[(fk['Lower Limit Filter'] == True) & (fk['Active Power Filter'] == True)]

# Sortiert DateFrame nach Bins (aufsteigend)
fk = fk.sort_values(by=['Identifier', 'Bin'], ascending = True)

df_f['BIN'] = fk['Bin']
df_f['Identifier'] = fk['Identifier']
df_f = df_f.drop_duplicates(ignore_index=True)

def n_counter(dataframe):
    fk_size = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].size()
    
    df_f['n'] = fk_size['size']

    print("n added")

def meaner(dataframe):
    fk_mean_p = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].mean()
    fk_mean_v = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Corrected Wind Speed'].mean()

    df_f['P'] = fk_mean_p['Active Power']
    df_f['V'] = fk_mean_v['Corrected Wind Speed']

    print("P added")
    print("V added")

def P_max(dataframe):
    fk_max = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].max()

    df_f['P max'] = fk_max['Active Power']
    
    print("P max added")

def P_min(dataframe):     
    fk_min = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].min()

    df_f['P min'] = fk_min['Active Power']

    print("P min added")
    
def P_std(dataframe):
    fk_std = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].std()
    
    df_f['P std'] = fk_std['Active Power']

    print("P std added")

def P_stdsqrtn():
    counter = 0
    i = 0

    for i in df_f['BIN']:
        n = df_f.at[counter, 'n']
        try:
            psqrt = df_f.at[counter, 'P std'] / (math.sqrt(n))
            df_f.at[counter, 'P std/sqrt(n)'] = psqrt
        except:
            continue
        counter += 1
    print("P std sqrt added")
        
        
def cp():
    counter = 0
    i = 0

    for i in range(len(df_f)):
        if df_f.at[counter, 'V'] != 0:
            cp = (df_f.at[counter, 'P'] * 1000) / ((0.5 * 1.225 * math.pi * ((fkpy.rotor_diameter / 2) ** 2)) * (df_f.at[counter, 'V'] ** 3))

            df_f.at[counter, 'cp'] = cp
        else:
            df_f.at[counter, 'cp'] = 0
        counter += 1
    return df_f
    print("cp added")


def nan_filler(dataframe):
    dataframe['BIN'] = dataframe['BIN'].fillna(0)
    dataframe['n'] = dataframe['n'].fillna(0)
    dataframe['cp'] = dataframe['cp'].fillna(0)
    dataframe['P max'] = dataframe['P max'].fillna(0)
    dataframe['P min'] = dataframe['P min'].fillna(0)
    dataframe['P std'] = dataframe['P std'].fillna(0)
    dataframe['P std/sqrt(n)'] = dataframe['P std/sqrt(n)'].fillna(0)


def export_df(dataframe):
    # Ändert die Datentypen von Float in Integer
    dataframe['BIN'] = dataframe['BIN'].astype(int)
    dataframe['n'] = dataframe['n'].astype(int)
    # Gibt das DataFrame mit n > 2 und nur mit der HK zurück
    dataframe = dataframe[(dataframe['n'] > 2) | (dataframe['Identifier'] == 'HK')]
    # Resettet die Indezies
    dataframe = dataframe.reset_index(drop = True)
    
    # Exportiert Jede Anlage als einzelne CSV-Datei
    date = datetime.now().strftime("%Y%m%d")
    my_exportFile = "./export/Bin/" + date + ".csv"
    vers = 0
    while os.path.isfile(my_exportFile):
        vers = vers + 1
        my_exportFile = "./export/Bin/" + date + "(" + str(vers) + ")" + ".csv"
    dataframe.to_csv(my_exportFile, sep=';', decimal=',')
    print(dataframe)

# Methods to run
n_counter(fk)
meaner(fk)
P_max(fk)
P_min(fk)
P_std(fk)
P_stdsqrtn()
cp()
df_f = df_f.append(twb_kennlinie)
nan_filler(df_f)
export_df(df_f)

print("Time for execution:", datetime.now() - fkpy.begin, "\n")
