# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:45:04 2022

@author: arda.ercan
"""

import pandas as pd
import tkinter as tk
#import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from datetime import datetime
import math
import matplotlib.pyplot as plt
from tqdm import tqdm

#from filter_kennl_2.py import *
import filter_kennl_2

fkpy = filter_kennl_2

fk = fkpy.df

# BIN = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
#        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
#        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
#        41, 42, 43, 44, 45, 46, 47, 48, 49, 50}

data = {'BIN': [],
        'V': [],
        'P': [],
        'n': [],
        'cp': [],
        'P max': [],
        'P min': [],
        'P std': [],
        'P std/sqrt(n)': []}

df_f = pd.DataFrame(data)
df_p = pd.DataFrame()


# df_f = df_f.set_index('BIN', drop=True, append=False, inplace=False, verify_integrity=False)

# def bin_num(df_f):
#     for b in range(1, 51):
#         df_f = df_f.loc[b, 'BIN']


def V_add(b, v, n):
    
    try:
        df_f.loc[b, 'V'] = v / n
    except:
        pass
    return df_f
    
def P_add(b, p, n):
    
    try:
        df_f.loc[b, 'P'] = p / n
    except:
        pass
    return df_f

def n_count(fk):
    for b in tqdm(range(1, 50)):
        val = 0
        n = 0
        v = 0
        p = 0
        for co in fk['Bin']:
            if fk.loc[val, 'Lower Limit Filter'] == True:
                if fk.loc[val, 'Active Power Filter'] == True:
                    if fk.loc[val, 'Bin'] == b:
                        v += fk.loc[val, 'Corrected Wind Speed']
                        p += fk.loc[val, 'Active Power']
                        
                        n += 1
                    
            val += 1
            if n > 3:
                # print("HALLO n > 3: ", n)
                df_f.loc[b, 'BIN'] = b
                df_f.loc[b, 'n'] = n
                V_add(b, v, n)
                P_add(b, p, n)
                P_max(df_f)
                P_min(df_f)
                P_std(df_f)
    # P_stdsqrtn()
            
        
def P_max(df_f):
    
    fk_max = fk.groupby(['Bin'], as_index=False)['Active Power'].max()

    # Counter
    co = 0
    x = 0
    y = 1
    for co in df_f['BIN']:
        try:
            if fk_max.loc[x, 'Bin'] == df_f.loc[y, 'BIN']:
                print("P MAX in Gange")
                df_f.loc[y, 'P max'] = fk_max.loc[x, 'Active Power']
                x += 1
                y += 1
            elif fk_max.loc[x, 'Bin'] < df_f.loc[y, 'BIN']:
                x += 1
            elif fk_max.loc[x, 'Bin'] > df_f.loc[y, 'BIN']:
                y += 1
        except:
            pass
    
            # print(df_f)

def P_min(df_f):
        # fk_min = fk.groupby(['Bin'], as_index=False).agg({'Active Power': ['min']})
        
        # if fk.loc[val, 'Lower Limit Filter'] == True:
        #             if fk.loc[val, 'Active Power Filter'] == True:
    fk_min = fk.groupby(['Bin'], as_index=False)['Active Power'].min()

    # Counter
    co = 0
    x = 0
    y = 1
    for co in df_f['BIN']:
        try:
            if fk_min.loc[x, 'Bin'] == df_f.loc[y, 'BIN']:
                print("P MIN in Gange")
                df_f.loc[y, 'P min'] = fk_min.loc[x, 'Active Power']
                x += 1
                y += 1
            elif fk_min.loc[x, 'Bin'] < df_f.loc[y, 'BIN']:
                x += 1
            elif fk_min.loc[x, 'Bin'] > df_f.loc[y, 'BIN']:
                y += 1
        except:
            pass
        
            # print(df_f)
        


def P_std(df_f):
    fk_std = fk.groupby(['Bin'], as_index=False)['Active Power'].std()

    # Counter
    co = 0
    x = 0
    y = 1
    for co in df_f['BIN']:
        try:
            if fk_std.loc[x, 'Bin'] == df_f.loc[y, 'BIN']:
                print("P STD in Gange")
                df_f.loc[y, 'P std'] = fk_std.loc[x, 'Active Power']
                x += 1
                y += 1
            elif fk_std.loc[x, 'Bin'] < df_f.loc[y, 'BIN']:
                x += 1
            elif fk_std.loc[x, 'Bin'] > df_f.loc[y, 'BIN']:
                y += 1
        except:
            pass
        
        # print(df_f)

def P_stdsqrtn():
    i=0
    for co in df_f['BIN']:
        # print("co: ", co)
        # print("i: ", i)
        n = df_f.loc[i, 'n']
        
        try:
            psqrt = df_f.loc[i, 'P std']**(1/n)
            # print("psqrt: ", psqrt)
            df_f.loc[i, 'P std/sqrt(n)'] = psqrt
            # print(df_f.loc[i, 'P std/sqrt(n)'])
        except:
            continue
        i+=1

# print(fk)
# co = 2
# fk[fk['DateTime']] = data_int
# for i in fk:
#     val = fk.loc[i, 'Pitch Angle']
#     if fk.isnull(val):
#         print("IST NULL")
#     else:
#         print("IST NICHT NULL")


# bin_num(df_f)
# print(df_f)


# fk = fk.sort_values('Bin', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)
# print(fk)
# print()
# fk = fk.set_index('Bin', drop=True, append=False, inplace=False, verify_integrity=False)
# print(fk)
# print()
# print()
# print(fk)

# print()
# fk_max = fk.sort_values('Bin', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)
# print(fk_max)
# print()


print(fk)
n_count(fk)
print()
print(df_f)


# print()
# print(df_f)
# print(df_p)
print("Time for execution:", datetime.now() - fkpy.begin, "\n")