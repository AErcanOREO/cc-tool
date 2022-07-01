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

import filter_correct_3 as fkpy

print('The Pandas version is {}.'.format(pd.__version__))

# Durchschnittsberechnung
# np.mean
# np.where
# pd.cut

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
rg_kennlinie = [{'Identifier': 'HK', 'V': 0, 'P': 0},
                 {'Identifier': 'HK', 'V': 1, 'P': 0},
                 {'Identifier': 'HK', 'V': 2, 'P': 0},
                 {'Identifier': 'HK', 'V': 3, 'P': 0},
                 {'Identifier': 'HK', 'V': 4, 'P': 161},
                 {'Identifier': 'HK', 'V': 5, 'P': 351},
                 {'Identifier': 'HK', 'V': 6, 'P': 635},
                 {'Identifier': 'HK', 'V': 7, 'P': 1026},
                 {'Identifier': 'HK', 'V': 8, 'P': 1544},
                 {'Identifier': 'HK', 'V': 9, 'P': 2204},
                 {'Identifier': 'HK', 'V': 10, 'P': 2910},
                 {'Identifier': 'HK', 'V': 11, 'P': 3399},
                 {'Identifier': 'HK', 'V': 12, 'P': 3656},
                 {'Identifier': 'HK', 'V': 13, 'P': 3776},
                 {'Identifier': 'HK', 'V': 14, 'P': 3780},
                 {'Identifier': 'HK', 'V': 15, 'P': 3780},
                 {'Identifier': 'HK', 'V': 16, 'P': 3780},
                 {'Identifier': 'HK', 'V': 17, 'P': 3780},
                 {'Identifier': 'HK', 'V': 18, 'P': 3780},
                 {'Identifier': 'HK', 'V': 19, 'P': 3690},
                 {'Identifier': 'HK', 'V': 20, 'P': 3600},
                 {'Identifier': 'HK', 'V': 21, 'P': 3600},
                 {'Identifier': 'HK', 'V': 22, 'P': 3600},
                 {'Identifier': 'HK', 'V': 23, 'P': 3600},
                 {'Identifier': 'HK', 'V': 24, 'P': 3564},
                 {'Identifier': 'HK', 'V': 25, 'P': 3528},
                 {'Identifier': 'HK', 'V': 26, 'P': 3087},
                 {'Identifier': 'HK', 'V': 27, 'P': 2646},
                 {'Identifier': 'HK', 'V': 28, 'P': 2205},
                 {'Identifier': 'HK', 'V': 29, 'P': 1764},
                 {'Identifier': 'HK', 'V': 30, 'P': 1323},
                 {'Identifier': 'HK', 'V': 31, 'P': 882},
                 {'Identifier': 'HK', 'V': 32, 'P': 441}]
'''

'''
mrk_kennlinie = [{'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': },
                {'Identifier': 'HK', 'V': , 'P': }]
'''

'''
avs_kennlinie = [{'Identifier': 'HK', 'V': 3.5, 'P': 0 },
                {'Identifier': 'HK', 'V': 4, 'P': 75 },
                {'Identifier': 'HK', 'V': 4.5, 'P': 194.2 },
                {'Identifier': 'HK', 'V': 5, 'P': 319.2 },
                {'Identifier': 'HK', 'V': 5.5, 'P': 463.3 },
                {'Identifier': 'HK', 'V': 6, 'P': 657.5 },
                {'Identifier': 'HK', 'V': 6.5, 'P': 856 },
                {'Identifier': 'HK', 'V': 7, 'P': 1126.4 },
                {'Identifier': 'HK', 'V': 7.5, 'P': 1391.4 },
                {'Identifier': 'HK', 'V': 8, 'P': 1684.5 },
                {'Identifier': 'HK', 'V': 8.5, 'P': 2076.8 },
                {'Identifier': 'HK', 'V': 9, 'P': 2425.2 },
                {'Identifier': 'HK', 'V': 9.5, 'P': 2807.1 },
                {'Identifier': 'HK', 'V': 10, 'P': 3220.9 },
                {'Identifier': 'HK', 'V': 10.5, 'P': 3689.1 },
                {'Identifier': 'HK', 'V': 11, 'P': 4181.3 },
                {'Identifier': 'HK', 'V': 11.5, 'P': 4612.4 },
                {'Identifier': 'HK', 'V': 12, 'P': 4902.4 },
                {'Identifier': 'HK', 'V': 12.5, 'P': 4980.3 },
                {'Identifier': 'HK', 'V': 13, 'P': 5047.7 },
                {'Identifier': 'HK', 'V': 13.6, 'P': 5056.9 },
                {'Identifier': 'HK', 'V': 14, 'P': 5056 },
                {'Identifier': 'HK', 'V': 14.4, 'P': 5086.1 },
                {'Identifier': 'HK', 'V': 15, 'P': 5097.2 },
                {'Identifier': 'HK', 'V': 15.6, 'P': 5108.3 },
                {'Identifier': 'HK', 'V': 16, 'P': 5127.2 },
                {'Identifier': 'HK', 'V': 16.4, 'P': 5145.5 },
                {'Identifier': 'HK', 'V': 17, 'P': 5125.5 },
                {'Identifier': 'HK', 'V': 17.4, 'P': 5116.4 },
                {'Identifier': 'HK', 'V': 18.1, 'P': 5064.2 },
                {'Identifier': 'HK', 'V': 18.5, 'P': 5097 },
                {'Identifier': 'HK', 'V': 19.1 'P': 5134.7 },
                {'Identifier': 'HK', 'V': 19.4 'P': 5075.9 },
                {'Identifier': 'HK', 'V': 19.8, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 21, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 22, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 23, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 24, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 25, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 26, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 27, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 28, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 29, 'P': 5113.1 },
                {'Identifier': 'HK', 'V': 30, 'P': 5113.1 }]
'''

'''
ava_kennlinie = [{'Identifier': 'HK', 'V': 0, 'P': 0},
                {'Identifier': 'HK', 'V': 4.1, 'P': 0},
                {'Identifier': 'HK', 'V': 4.2, 'P': 104.37},
                {'Identifier': 'HK', 'V': 4.5, 'P': 252.13},
                {'Identifier': 'HK', 'V': 5, 'P': 369.08},
                {'Identifier': 'HK', 'V': 5.5, 'P': 490.98},
                {'Identifier': 'HK', 'V': 6, 'P': 754.6},
                {'Identifier': 'HK', 'V': 6.6, 'P': 1047.49},
                {'Identifier': 'HK', 'V': 7, 'P': 1317.27},
                {'Identifier': 'HK', 'V': 7.5, 'P': 1593.35},
                {'Identifier': 'HK', 'V': 8, 'P': 1892.65},
                {'Identifier': 'HK', 'V': 8.5, 'P': 2248.87},
                {'Identifier': 'HK', 'V': 9, 'P': 2604.76},
                {'Identifier': 'HK', 'V': 9.5, 'P': 3119.59},
                {'Identifier': 'HK', 'V': 10, 'P': 3535.78},
                {'Identifier': 'HK', 'V': 10.5, 'P': 3880.29},
                {'Identifier': 'HK', 'V': 11, 'P': 4453.5},
                {'Identifier': 'HK', 'V': 11.5, 'P': 4832.56},
                {'Identifier': 'HK', 'V': 12, 'P': 5022.07},
                {'Identifier': 'HK', 'V': 13.1, 'P': 5033.45},
                {'Identifier': 'HK', 'V': 13.4, 'P': 5042.06},
                {'Identifier': 'HK', 'V': 14, 'P': 5032.94},
                {'Identifier': 'HK', 'V': 14.5, 'P': 5036.3},
                {'Identifier': 'HK', 'V': 15, 'P': 5034.02},
                {'Identifier': 'HK', 'V': 15.6, 'P': 5036.35},
                {'Identifier': 'HK', 'V': 16.2, 'P': 5035.71},
                {'Identifier': 'HK', 'V': 16.5, 'P': 5034.26},
                {'Identifier': 'HK', 'V': 17, 'P': 5034.78},
                {'Identifier': 'HK', 'V': 17.6, 'P': 5034.47},
                {'Identifier': 'HK', 'V': 25, 'P': 5034.47}]
'''
# print(pd.cut(df_f['V'], [0,2,3,4,5,6,8],labels=False))

# Wenn Active Power Filter aus ist sind die BINS zwischen 6-13 wieder richtig drinne
# V ist bis auf die 2 oder 3 Kommastelle richtig
# Rest nicht!!!

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
    '''
    i = 0
    counter_size = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_size.at[counter_size, 'Bin'] == df_f.at[counter_df, 'BIN']:
                print("IF")
                df_f.at[counter_df, 'n'] = fk_size.at[counter_size, 'size']
                counter_size += 1
                counter_df += 1
            elif fk_size.at[counter_size, 'Bin'] < df_f.at[counter_df, 'BIN']:
                print("1 ELIF")
                counter_size += 1
            elif fk_size.at[counter_size, 'Bin'] > df_f.at[counter_df, 'BIN']:
                print("2 ELIF")
                counter_df += 1
        except:
            continue
    df_f['n'] = fk_size['size']
    print(df_f)'''

def meaner(dataframe):
    fk_mean_p = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].mean()
    fk_mean_v = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Corrected Wind Speed'].mean()
    #print(fk_mean_p)
    #print(fk_mean_v)
    df_f['P'] = fk_mean_p['Active Power']
    df_f['V'] = fk_mean_v['Corrected Wind Speed']

    print("P added")
    print("V added")

'''
    i = 0
    counter_mean = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_mean.at[counter_mean, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P'] = fk_mean.at[counter_mean, 'Active Power']
                df_f.at[counter_df, 'V'] = fk_mean.at[counter_mean, 'Corrected Wind Speed']
                counter_mean += 1
                counter_df += 1
            elif fk_mean.at[counter_mean, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_mean += 1
            elif fk_mean.at[counter_mean, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
        
    print("P mean added")'''


def P_max(dataframe):
    fk_max = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].max()

    df_f['P max'] = fk_max['Active Power']
    
    print("P max added")

    # max_val = (lambda b, i, df, df_f: df['Active Power'] if b['Bin'] == df_f['BIN'], fk_max, df_f)
    # df_f['P max'] = df_f.apply(filter(list(lambda fk_max['Active Power'], df_f['BIN']: fk_max['Active Power'] if df_f['BIN'] == fk_max['Bin'] else continue)), fk_max, df_f, )
    '''
    i = 0
    counter_max = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_max.at[counter_max, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P max'] = fk_max.at[counter_max, 'max']
                counter_max += 1
                counter_df += 1
            elif fk_max.at[counter_max, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_max += 1
            elif fk_max.at[counter_max, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P max added")
            # print(df_f)'''

def P_min(dataframe):
        # fk_min = fk.dataframeby(['Bin'], as_index=False).agg({'Active Power': ['min']})
        
    fk_min = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].min()

    df_f['P min'] = fk_min['Active Power']

    print("P min added")
    
    '''
    # Counter
    i = 0
    counter_min = 0
    counter_df = 0
    for i in df_f['BIN']:
        try:
            if fk_min.at[counter_min, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P min'] = fk_min.at[counter_min, 'min']
                counter_min += 1
                counter_df += 1
            elif fk_min.at[counter_min, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_min += 1
            elif fk_min.at[counter_min, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P min added")
            # print(df_f) '''
        

def P_std(dataframe):
    fk_std = dataframe.groupby(['Identifier', 'Bin'], as_index=False)['Active Power'].std()
    
    df_f['P std'] = fk_std['Active Power']

    print("P std added")

    '''
    # Counter
    i = 0
    counter_std = 0
    counter_df = 0
    for i in range(len(df_f)):
        try:
            if fk_std.at[counter_std, 'Bin'] == df_f.at[counter_df, 'BIN']:
                df_f.at[counter_df, 'P std'] = fk_std.at[counter_std, 'std']
                counter_std += 1
                counter_df += 1
            elif fk_std.at[counter_std, 'Bin'] < df_f.at[counter_df, 'BIN']:
                counter_std += 1
            elif fk_std.at[counter_std, 'Bin'] > df_f.at[counter_df, 'BIN']:
                counter_df += 1
        except:
            continue
    print("P std added")
        # print(df_f)'''

def P_stdsqrtn():
    
    counter = 0
    i = 0
    for i in df_f['BIN']:
        n = df_f.at[counter, 'n']
        try:
            psqrt = df_f.at[counter, 'P std'] / (math.sqrt(n))
            #psqrt = float("{:.2f}".format(psqrt))
            df_f.at[counter, 'P std/sqrt(n)'] = psqrt
                # print(df_f.at[i, 'P std/sqrt(n)'])

            #print("ID: ", df_f.at[counter, 'Identifier'])
            #print("BIN: ", df_f.at[counter, 'BIN'])
            #print("n: ", n)
            #print("erg: ", psqrt)
            #print()
            
        except:
            continue
        counter+=1
    print("P std sqrt added")
        
        
def cp():
    counter = 0
    i = 0
    for i in range(len(df_f)):
        # print("i:", i)
        # print("df_f.at[counter, 'V']: ", df_f.at[counter, 'V'])
        if df_f.at[counter, 'V'] != 0:
            # print("sind in if")
            # # try:
            # print("try block")
            # print("df_f.at[counter, 'P']: ", df_f.at[counter, 'P'])
            # print("df_a.at berechnung", (df_f.at[counter, 'P'] * 1000) / ((0.5 * 1.225 * math.pi * ((fkpy.rotor_diameter / 2) ** 2)) * (df_f.at[counter, 'V'] ** 3)))
            cp = (df_f.at[counter, 'P'] * 1000) / ((0.5 * 1.225 * math.pi * ((fkpy.rotor_diameter / 2) ** 2)) * (df_f.at[counter, 'V'] ** 3))
            # print("cp: ", cp)
         
            # except:
                # print("Sind in Except drinne!:DASD")
                # continue
            df_f.at[counter, 'cp'] = cp
        else:
            # print("sind in else")
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


    #date = datetime.now().strftime("%Y%m%d")
    #my_exportFile = "./export/Bin/" + date + ".csv"
    #vers = 0
    #while os.path.isfile(my_exportFile):
    #    vers = vers + 1
    #    my_exportFile = "./export/Bin/" + date + "(" + str(vers) + ")" + ".csv"
    #dataframe.to_csv(my_exportFile, sep=';', decimal=',')


    print(dataframe)



# Methods to run
n_counter(fk)
meaner(fk)
P_max(fk)
P_min(fk)
P_std(fk)
P_stdsqrtn()
cp()
#nan_filler(df_f)
df_f = df_f.append(twb_kennlinie)
nan_filler(df_f)
#df_f = df_f.reset_index(drop=True)
export_df(df_f)





#print("BIN 11:")
#print(df_f[(df_f['Identifier'] == 'BW 28') & (df_f['BIN'] == 11)])

#print("BIN 12:")
#print(df_f[(df_f['Identifier'] == 'BW 28') & (df_f['BIN'] == 12)])



#print(df_res[df_res['Identifier'] == 'BW 28'])

#print(fk[(fk['Identifier'] == 'BW 28') & (fk['Bin'] == 29)])

#print(df_f[df_f['Identifier'] == 'BW 05'])

