# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:35:53 2022

@author: arda.ercan
"""

import pandas as pd
# import tkinter as tk
# from PIL import Image, ImageTk
# from tkinter.filedialog import askopenfile
from datetime import datetime
import math
# import matplotlib.pyplot as plt
import os.path
from tqdm import tqdm

#plotly express

import filter_kennl_final


# Durchschnittsberechnung
# np.mean
# np.where
# pd.cut


fkpy = filter_kennl_final
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
df_res = pd.DataFrame(data)

twb_kennlinie = [{'Identifier': 'HK', 'V': 3.5, 'P': 5.112170643 },
                  {'Identifier': 'HK', 'V': 4, 'P': 126.5348803 },
                  {'Identifier': 'HK', 'V': 5, 'P': 457.1223788 },
                  {'Identifier': 'HK', 'V': 6, 'P': 1007.110478 },
                  {'Identifier': 'HK', 'V': 7, 'P': 1743.022208 },
                  {'Identifier': 'HK', 'V': 8, 'P': 2642.228084 },
                  {'Identifier': 'HK', 'V': 9, 'P': 3746.834988 },
                  {'Identifier': 'HK', 'V': 10, 'P': 5092.412141},
                  {'Identifier': 'HK', 'V': 11.5, 'P': 6245.352513},
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
                  {'Identifier': 'HK', 'V': 29, 'P':   6386.350148}]



print(pd.cut(df_f['V'], [0,2,3,4,5,6,8],labels=False))

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
    for f in tqdm(df['V']):
        if f != 0:
            try:
                val = 2 + int((f - 0.25) / 0.5)
                df.at[counter, 'BIN'] = val
            except:
                df.at[counter, 'BIN'] = 0
        counter += 1
    print("df_bin end")
    return df



# Wenn Active Power Filter aus ist sind die BINS zwischen 6-13 wieder richtig drinne
# V ist bis auf die 2 oder 3 Kommastelle richtig
# Rest nicht!!!

fk = fk[(fk['Lower Limit Filter'] == True) & (fk['Active Power Filter'] == True)]

# Sortiert DateFrame nach Bins (aufsteigend)
fk = fk.sort_values(by=['Identifier', 'Bin'], ascending = True)


def n_count(dataframe):
    global df_res
    counter = 0
    y = 0
    n = 0
    v = 0
    p = 0
    for i in tqdm(range(0, len(dataframe))):        
        if dataframe.at[counter, 'Bin'] == dataframe.at[i, 'Bin']:
            v += dataframe.at[counter, 'Corrected Wind Speed']
            p += dataframe.at[counter, 'Active Power']
            n += 1  
        if dataframe.at[counter, 'Bin'] != dataframe.at[counter + 1, 'Bin']:
            df_f.at[y, 'n'] = n
            df_f.at[y, 'BIN'] = dataframe.at[counter, 'Bin']
            try:
                df_f.at[y, 'V'] = float(v / n)
                df_f.at[y, 'P'] = float(p / n)
            except:
                continue
         
            y += 1
            n = 0
            v = 0
            p = 0
        counter += 1
        
        if counter == (len(dataframe)-1):
            counter -= 1
            y2 = y
            v = 0
            p = 0
            n = 0
            neg_counter = len(dataframe) - 1
            neg_counter2 = neg_counter - 1
            
            while dataframe.at[neg_counter, 'Bin'] == dataframe.at[neg_counter2, 'Bin']:
                v += dataframe.at[neg_counter, 'Corrected Wind Speed']
                p += dataframe.at[neg_counter, 'Active Power']
                n += 1
                    
                if dataframe.at[neg_counter2, 'Bin'] != dataframe.at[neg_counter2-1, 'Bin']:
                    v += dataframe.at[neg_counter2, 'Corrected Wind Speed']
                    p += dataframe.at[neg_counter2, 'Active Power']
                    n += 1
                    
                    df_f.at[y2, 'BIN'] = dataframe.at[neg_counter, 'Bin']
                    df_f.at[y2, 'V'] = float(v / n)
                    df_f.at[y2, 'P'] = float(p / n)
                    df_f.at[y2, 'n'] = n
                    # break
                
                neg_counter -= 1
                neg_counter2 -= 1
                
    print("V added")
    print("P added")
    print("n added")
    P_max(group)
    P_min(group)
    P_std(group)
    P_stdsqrtn()
    cp()
    print("n count ist zu ende!")
    df_f['Identifier'] = name
    
    # print("n count hat df_f")
    # print(df_f)
    # print("n count hat df_res")
    # print(df_res)
    for i in range(len(df_f)):
        new_row = {'BIN': df_f.at[i, 'BIN'], 'Identifier': df_f.at[i, 'Identifier'], 'V': df_f.at[i, 'V'], 'P': df_f.at[i, 'P'],
                   'n': df_f.at[i, 'n'], 'cp': df_f.at[i, 'cp'], 'P max': df_f.at[i, 'P max'],
                   'P min': df_f.at[i, 'P min'], 'P std': df_f.at[i, 'P std'], 'P std/sqrt(n)': df_f.at[i, 'P std/sqrt(n)']}
        # hinzufügen der Zeilen in das dataframe
        df_res = df_res.append(new_row, ignore_index=True)    
        
    # if export:
        # export_df(df_f, name)
        
    


def P_max(dataframe):
    fk_max = dataframe.groupby(['Bin', 'Identifier'], as_index=False)['Active Power'].max()
    
    # max_val = (lambda b, i, df, df_f: df['Active Power'] if b['Bin'] == df_f['BIN'], fk_max, df_f)
    # df_f['P max'] = df_f.apply(filter(list(lambda fk_max['Active Power'], df_f['BIN']: fk_max['Active Power'] if df_f['BIN'] == fk_max['Bin'] else continue)), fk_max, df_f, )
    i = 0
    counter_max = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_max.at[counter_max, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P max'] = fk_max.at[counter_max, 'Active Power']
                counter_max += 1
                counter_df += 1
            elif fk_max.at[counter_max, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_max += 1
            elif fk_max.at[counter_max, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P max added")
            # print(df_f)

def P_min(dataframe):
        # fk_min = fk.dataframeby(['Bin'], as_index=False).agg({'Active Power': ['min']})
        
        # if fk.at[val, 'Lower Limit Filter'] == True:
        #             if fk.at[val, 'Active Power Filter'] == True:
    fk_min = dataframe.groupby(['Bin', 'Identifier'], as_index=False)['Active Power'].min()
    
    # Counter
    i = 0
    counter_min = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_min.at[counter_min, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P min'] = fk_min.at[counter_min, 'Active Power']
                counter_min += 1
                counter_df += 1
            elif fk_min.at[counter_min, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_min += 1
            elif fk_min.at[counter_min, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P min added")
            # print(df_f)
        


def P_std(dataframe):
    fk_std = dataframe.groupby(['Bin'], as_index=False)['Active Power'].std()
    
    # Counter
    i = 0
    counter_std = 0
    counter_df = 0
    for i in range(len(df_f)):
        try:
            if fk_std.at[counter_std, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P std'] = fk_std.at[counter_std, 'Active Power']
                counter_std += 1
                counter_df += 1
            elif fk_std.at[counter_std, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_std += 1
            elif fk_std.at[counter_std, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P std added")
        # print(df_f)

def P_stdsqrtn():
    counter = 0
    i = 0
    for i in df_f['BIN']:
        n = df_f.at[counter, 'n']
        try:
            psqrt = df_f.at[counter, 'P std'] / math.sqrt(n)
            df_f.at[counter, 'P std/sqrt(n)'] = psqrt
                # print(df_f.at[i, 'P std/sqrt(n)'])    
        except:
            continue
        counter+=1
    print("P std sqrt added")
        
        
def cp():
    counter = 0
    i = 0
    for i in df_f['BIN']:
        try:
            if df_f.at[counter, 'V'] != 0:
                df_f.at[counter, 'cp'] = (df_f.at[counter, 'P'] * 1000) / ((0.5 * 1.225 * math.pi * ((fkpy.rd / 2) ** 2)) * (df_f.at[counter, 'V'] ** 3))
            else:
                df_f.at[counter, 'cp'] = 0
        except:
            continue
        counter += 1
    print("cp added")


def nan_filler(dataframe):
    dataframe['n'] = dataframe['n'].fillna(0)
    dataframe['cp'] = dataframe['cp'].fillna(0)
    dataframe['P max'] = dataframe['P max'].fillna(0)
    dataframe['P min'] = dataframe['P min'].fillna(0)
    dataframe['P std'] = dataframe['P std'].fillna(0)
    dataframe['P std/sqrt(n)'] = dataframe['P std/sqrt(n)'].fillna(0)


def export_df(dataframe, name):
    dataframe['BIN'] = dataframe['BIN'].astype(int)
    dataframe['n'] = dataframe['n'].astype(int)
    dataframe = dataframe[(dataframe['n'] > 2) | (dataframe['Identifier'] == 'HK')
                          ]
    dataframe = dataframe.reset_index(drop = True)
    
    # Exportiert Jede Anlage als einzelne CSV-Datei
    date = datetime.now().strftime("%Y%m%d")
    my_exportFile = "./export/Bin/" + date + ".csv"
    vers = 0
    while os.path.isfile(my_exportFile):
        vers = vers + 1
        my_exportFile = "./export/Bin/" + name + " " + date + "(" + str(vers) + ")" + ".csv"
    dataframe.to_csv(my_exportFile, sep=';', decimal=',')
    print("WEA exported: ", name)
    
    print(dataframe)
    return dataframe


grouped_df = fk.groupby('Identifier')
# n_count(grouped_df)
# print("grouped_df", grouped_df)
for name, group in grouped_df:
    # print("name: ", name)
    group = group.reset_index(drop = True)
    # print("group: ", group)
    n_count(group)


df_res = df_res.append(twb_kennlinie, ignore_index = True)

df_bin(df_res)

# nan_filler(df_res)

df_res = df_res.fillna(0)
export_df(df_res, name)
    

print("Time for execution:", datetime.now() - fkpy.begin, "\n")

# print(df_res)
# print("Summe der Anzahl: ", df_f['n'].sum())
'''
df_len = len(df)
    for i in range(df_len):
        if y == df_len:
            y -= 1
            start = x - co
            sumDau(start, df_len-1, df)
            gesErt(start, df_len-1, df)
            anzEnt(start, df_len-1, df)
            dauEnt(start, df_len-1, df)
            co = 0
            
        if df.iat[x, 0] == df.iat[y, 0]:
            co += 1

        elif df.iat[x, 0] != df.iat[y, 0]:
            start = x - co
            sumDau(start, x, df)
            gesErt(start, x, df)
            anzEnt(start, x, df)
            dauEnt(start, x, df)
            
            co = 0
       
        x+=1
        y+=1
'''

        
# def use_filter(fk):
#     counter = 0
#     for i in fk['Bin']:
#         # print("i: ", i)
#         if fk.at[counter, 'Lower Limit Filter'] == True:
#             print("fk.at[counter, 'Lower Limit Filter']: ", fk.at[counter, 'Lower Limit Filter'])
#             if fk.at[counter, 'Active Power Filter'] == True:
#                 print("Beides True")
#                 print("counter: ", counter)
#                 print("fk.at[counter, 'Active Power Filter']: ", fk.at[counter, 'Active Power Filter'])
#         counter += 1
#     print(fk)
        

# def V_add(b, v, n):
#     '''
#     =MITTELWERTWENN($P$12:$P$52715;Y$1;$N$12:$N$52715)

#     =WENN(
#         WVERWEIS($A11 ; 'filtered data + bin averaging'!$T$1:$CV$8 ; 4 ; FALSCH) >= 3 ; WVERWEIS($A11 ; 'filtered data + bin averaging'!$T$1:$CV$8 ; 2 ; FALSCH) ; "")
#     '''
#     try:
#         df_f.at[b, 'V'] = float(v / n)
#     except:
#         pass
#     return df_f
    

# def P_add(b, p, n):
    
#     try:
#         df_f.at[b, 'P'] = float(p / n)
#     except:
#         pass
#     return df_f



'''
fkpy = filter_kennl_2
fk = fkpy.df

export = True

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
df_res = pd.DataFrame(data)
# Wenn Active Power Filter aus ist sind die BINS zwischen 6-13 wieder richtig drinne
# V ist bis auf die 2 oder 3 Kommastelle richtig
# Rest nicht!!!
fk = fk[(fk['Lower Limit Filter'] == True) & (fk['Active Power Filter'] == True)]

# Sortiert DateFrame nach Bins (aufsteigend)
fk = fk.sort_values(by=['Identifier', 'Bin'], ascending = True)
# print("SORTIERT NACH IDENTIFIER UND BIN!")
# print(fk)
# print()


Vorherige Versuche, nur die True-Werte zu behalten
fk = fk.drop(fk[fk['Lower Limit Filter'] == False].index, inplace = True, axis=1)

filtertouse = fk[ (fk['Lower Limit Filter'] == False) & (fk['Active Power Filter'] == False) ].index
fk_new = fk.drop(filtertouse, inplace = False)


# Resettet die vorherigen Indexe und setzt neue Indexe
fk = fk.reset_index(drop = True)
# print(fk)



# Versuche FK in Gruppen aufzuteilen
# gfk = fk.groupby(fk.Identifier)

# print("DAS IST GFK:!")
# print(gfk)
# print()

# for i in range(0,5):
#     pic = gfk.get_group(('BW 05', 'BW 07'))
#     print("das ist Pic!")
#     print(pic)
#     print()

def n_count(fk):
    global df_res
    counter = 0
    y = 0
    n = 0
    v = 0
    p = 0
    for i in tqdm(range(0, len(fk))):        
        # df_f['Identifier'] = group['Identifier']
        # print("i: ", i)
        # print("fk.at[counter, 'Lower Limit Filter']: ", fk.at[counter, 'Lower Limit Filter'])
        # print("fk.at[counter, 'Active Power Filter']: ", fk.at[counter, 'Active Power Filter'])
        # print("fk.at[counter, 'Bin']: ", fk.at[counter, 'Bin'])
        # print()
        
        if fk.at[counter, 'Bin'] == fk.at[i, 'Bin']:
            v += fk.at[counter, 'Corrected Wind Speed']
            p += fk.at[counter, 'Active Power']
            n += 1
            
            # print("v: ", v)
            # print("p: ", p)
            # print("Counter: ", counter)
            # print("Anzahl: ", n)       
        if fk.at[counter, 'Bin'] != fk.at[counter + 1, 'Bin']:
            df_f.at[y, 'n'] = n
            df_f.at[y, 'BIN'] = fk.at[counter, 'Bin']
            try:
                df_f.at[y, 'V'] = float(v / n)
                df_f.at[y, 'P'] = float(p / n)
            except:
                continue
         
            y += 1
            n = 0
            v = 0
            p = 0
        counter += 1
        
        if counter == (len(fk)-1):
            counter -= 1
            y2 = y
            v = 0
            p = 0
            n = 0
            neg_counter = len(fk) - 1
            neg_counter2 = neg_counter - 1
            
            while fk.at[neg_counter, 'Bin'] == fk.at[neg_counter2, 'Bin']:
                # print()
                # print("neg_counter: ", neg_counter)
                # print()
                # print("fk.at[neg_counter, 'Bin']: ", fk.at[neg_counter, 'Bin'])
                # print("fk.at[neg_counter, 'Active Power']: ", fk.at[neg_counter, 'Active Power'])
                # print()
                # print("fk.at[neg_counter2, 'Bin']: ", fk.at[neg_counter2, 'Bin'])
                # print("fk.at[neg_counter2, 'Active Power']: ", fk.at[neg_counter2, 'Active Power'])
                # print()
                # print("fk.at[neg_counter, 'Corrected Wind Speed']: ", fk.at[neg_counter, 'Corrected Wind Speed'])
                # print("fk.at[neg_counter, 'Active Power']: ", fk.at[neg_counter, 'Active Power'])
                
                v += fk.at[neg_counter, 'Corrected Wind Speed']
                p += fk.at[neg_counter, 'Active Power']
                n += 1
                    
                if fk.at[neg_counter2, 'Bin'] != fk.at[neg_counter2-1, 'Bin']:
                    v += fk.at[neg_counter2, 'Corrected Wind Speed']
                    p += fk.at[neg_counter2, 'Active Power']
                    n += 1
                    
                    df_f.at[y2, 'BIN'] = fk.at[neg_counter, 'Bin']
                    df_f.at[y2, 'V'] = float(v / n)
                    df_f.at[y2, 'P'] = float(p / n)
                    df_f.at[y2, 'n'] = n
                    # break
                
                neg_counter -= 1
                neg_counter2 -= 1
                # print("Negative Counter: ", fk.at[neg_counter, 'Active Power'])
                # print("len fk -1: ", fk.at[len(fk)-1, 'Active Power'])
                          
            # print("Counter-1 : ", fk.at[counter, 'Active Power'])
        
      
    print("V added")
    print("P added")
    print("n added")
    P_max(group)
    P_min(group)
    P_std(group)
    P_stdsqrtn()
    cp()
    print("n count ist zu ende!")
    print("DateFrame dazu: ")
    df_f['Identifier'] = name
    for i in range(len(df_f)):
        new_row = {'BIN': df_f.at[i, 'BIN'], 'Identifier': df_f.at[i, 'Identifier'], 'V': df_f.at[i, 'V'], 'P': df_f.at[i, 'P'],
                   'n': df_f.at[i, 'n'], 'cp': df_f.at[i, 'cp'], 'P max': df_f.at[i, 'P max'],
                   'P min': df_f.at[i, 'P min'], 'P std': df_f.at[i, 'P std'], 'P std/sqrt(n)': df_f.at[i, 'P std/sqrt(n)']}
                    # hinzufügen der Zeilen in das dataframe
        
        df_res = df_res.append(new_row, ignore_index=True)
        # df_res = df_res.append(new_row, ignore_index=True)
    
   
    # finalize_df(df_f)
    # finalize_df(df_res)
    
    # print()
    # print("DF_F")
    # print(df_f)
    if export:
        export_df(df_f, name)
        export_df(df_res, name)
    # df_res.concat([df_f], ignore_index = True)
    

            
        
def P_max(group):
    fk_max = group.groupby(['Bin', 'Identifier'], as_index=False)['Active Power'].max()
    # Counter
    i = 0
    counter_max = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_max.at[counter_max, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P max'] = fk_max.at[counter_max, 'Active Power']
                counter_max += 1
                counter_df += 1
            elif fk_max.at[counter_max, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_max += 1
            elif fk_max.at[counter_max, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P max added")
            # print(df_f)

def P_min(group):
        # fk_min = fk.groupby(['Bin'], as_index=False).agg({'Active Power': ['min']})
        
        # if fk.at[val, 'Lower Limit Filter'] == True:
        #             if fk.at[val, 'Active Power Filter'] == True:
    fk_min = group.groupby(['Bin', 'Identifier'], as_index=False)['Active Power'].min()
    
    # Counter
    i = 0
    counter_min = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_min.at[counter_min, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P min'] = fk_min.at[counter_min, 'Active Power']
                counter_min += 1
                counter_df += 1
            elif fk_min.at[counter_min, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_min += 1
            elif fk_min.at[counter_min, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P min added")
            # print(df_f)
        


def P_std(group):
    fk_std = group.groupby(['Bin'], as_index=False)['Active Power'].std()
    
    # Counter
    i = 0
    counter_std = 0
    counter_df = 0
    for i in range(len(df_f)):
        try:
            if fk_std.at[counter_std, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P std'] = fk_std.at[counter_std, 'Active Power']
                counter_std += 1
                counter_df += 1
            elif fk_std.at[counter_std, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_std += 1
            elif fk_std.at[counter_std, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P std added")
        # print(df_f)

def P_stdsqrtn():
    counter = 0
    i = 0
    for i in df_f['BIN']:
        n = df_f.at[counter, 'n']
        try:
            psqrt = df_f.at[counter, 'P std'] / math.sqrt(n)
            df_f.at[counter, 'P std/sqrt(n)'] = psqrt
                # print(df_f.at[i, 'P std/sqrt(n)'])    
        except:
            continue
        counter+=1
    print("P std sqrt added")
        
        
def cp():
    counter = 0
    i = 0
    for i in df_f['BIN']:
        try:
            if df_f.at[counter, 'V'] != 0:
                df_f.at[counter, 'cp'] = (df_f.at[counter, 'P'] * 1000) / ((0.5 * 1.225 * math.pi * ((fkpy.rd / 2) ** 2)) * (df_f.at[counter, 'V'] ** 3))
            else:
                df_f.at[counter, 'cp'] = 0
        except:
            continue
        counter += 1
    print("cp added")


# def finalize_df(df):
    
#     # print("DF:")
#     # print(df)
#     # print("DF Finalized!")
#     return df
    

def export_df(dataframe, name):
    dataframe['BIN'] = dataframe['BIN'].astype(int)
    dataframe['n'] = dataframe['n'].astype(int)
    dataframe = dataframe[dataframe['n'] > 2]
    dataframe = dataframe.reset_index(drop = True)
    # Exportiert Jede Anlage als einzelne CSV-Datei
    # date = datetime.now().strftime("%Y%m%d")
    # my_exportFile = "./export/Bin/" + name + " " + date + ".csv"
    # vers = 0
    # while os.path.isfile(my_exportFile):
    #     vers = vers + 1
    #     my_exportFile = "./export/Bin/" + name + " " + date + "(" + str(vers) + ")" + ".csv"
    # dataframe.to_csv(my_exportFile, sep=';', decimal=',')
    print("WEA exported: ", name)
    print(dataframe)


grouped_df = fk.groupby('Identifier')

for name, group in grouped_df:
    # print("name: ", name)
    group = group.reset_index(drop = True)
    # print("group: ", group)
    n_count(group)


print("Time for execution:", datetime.now() - fkpy.begin, "\n")
'''

'''
### Herstellekennlinien der Anlagen ###
Alte Ausführung (Alle in eine Zeile)
twb_her_kenn = {
    'Identifier': ['HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 
                    'HK', 'HK', 'HK', 'HK', 'HK'],
    'V':          [3.5, 4, 5, 6,
                      7, 8, 9, 10,
                      11, 11.5, 12, 13,
                      14, 15, 16, 17,
                      18, 19, 20, 21, 
                      22, 23, 24, 25, 
                      26, 27, 28, 29, 30],
    'P':          [5.112170643, 126.5348803, 457.1223788, 1007.110478,
                    1743.022208, 2642.228084, 3746.834988, 5092.412141,
                    6245.352513, 6386.350148, 6386.350148, 6386.350148,
                    6386.350148, 6386.350148, 6386.350148, 6386.350148,
                    6386.350148, 6386.350148, 6386.350148, 6386.350148,
                    6386.350148, 6386.350148, 6386.350148, 6386.350148,
                    6386.350148,6386.350148, 6386.350148, 6386.350148, 6386.350148]}

df_f = df_f.append(twb_her_kenn, ignore_index=True)
'''