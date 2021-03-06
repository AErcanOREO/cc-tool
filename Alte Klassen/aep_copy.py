# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 14:13:02 2022

@author: arda.ercan
"""

from ast import Index
import telnetlib
import pandas as pd
#from tqdm import tqdm
import filter_correct_3 as fk
import bin_averaging_4 as ba
import numpy as np
from scipy.stats import weibull_min, weibull_max
import math
from scipy.stats import exponweib


data = {'Bin':[],
        'Identifier':[],
        'V':[],
        'V extended':[],
        'P':[],
        '(Pi-1+Pi)/2':[],
        'f':[],
        'f extended':[]}


df = pd.DataFrame(data)
df['Bin'] = ba.df_f['BIN']
df['Identifier'] = ba.df_f['Identifier']
df['V'] = ba.df_f['V']
df['P'] = ba.df_f['P']


def rower():
    global df
    df = df.sort_values(['Identifier', 'Bin', 'V'])
    id_df = df.drop_duplicates('Identifier')
    counter = 0

    for i in id_df['Identifier']:
        df_len = len(df)

        df.at[df_len+counter, 'Identifier'] = i
        df.at[df_len+counter, 'Bin'] = 0
        df.at[df_len+counter, 'P'] = 0
        df.at[df_len+counter, 'V extended'] = 0
        df.at[df_len+counter, 'f extended'] = 0

        #df = pd.concat(row_new)
        #df = df.append(new_row, ignore_index=False)
        counter += 1
    df = df.drop([df_len+counter-1])
    df = df.sort_values(by=['Identifier', 'Bin', 'P'], ascending = True)

def cacu():
    counter = 0
    for value in df['V']:
        #print("I:")
        #print(value)
        #print("df.at[counter, 'V']: ", df.at[counter, 'V'])
        if math.isnan(value):
            #print("SChleife")
            #print("I:")
            #print(value)
            erg = df.at[counter + 1, 'V'] - 0.5
            #print("ERG=")
            #print(erg)
            df.at[counter, 'V'] = erg
            
        else:
            pass
        counter += 1



#df.index = df.index + 1

#print("DF INDEX + 1")
#print(df.index)


#df.at[0, 'Identifier'] = df.at[1, 'Identifier']


#if df.at[1, 'V'] - 0.5 > 0:
 #       df.at[0, 'V'] = df.at[1, 'V'] - 0.5
  #      df.at[0, 'P'] = 0

#df = df.sort_index()


#print("fd",ba.df_f)
#print("df",df)
#print("fd.df_f",ba.df_f)


'''=SVERWEIS(was Sie nachschlagen m??chten;
             wo Sie nachschlagen m??chten;
             Spaltennummer im Bereich mit dem R??ckgabewert;
             ungef??hre oder genaue Entsprechung zur??ckgeben ??? angegeben als "1/WAHR" oder "0/FALSCH").
'''


'''
Bin:
'result bin averaged power curve'!$N$2 = MIN(BIN Wert aus bin averaging)

'result bin averaged power curve'!$N$5 = MAX(BIN Wert aus bin averaging)
'result bin averaged power curve'!$A$4:$I$84 = Ganze Tabelle aus bin averaging


bin 6    =SVERWEIS('result bin averaged power curve'!$N$2;'result bin averaged power curve'!$A$4:$I$84;1;FALSCH)

bin 7 und weiter    =MIN(A5+1;SVERWEIS('result bin averaged power curve'!$N$5;'result bin averaged power curve'!$A$4:$I$84;1;FALSCH))
'''
def v_extended():
    counter = 1
    df_counter = 1
    for i in range(len(df['Bin'])):
        if df.at[counter - 1, 'Identifier'] == df.at[counter, 'Identifier']:
            if df.at[counter - 1, 'Bin'] + 1 == df.at[counter, 'Bin']:
                pass
            else:
                df.at[len(df) + df_counter, 'V extended'] = 30
            # if df.at[counter - 1, 'Bin'] += 1 == df.at[counter, 'Bin']

'''
(Pi-1+pi)/2:
    
bin 5    =MITTELWERT(D4:D5)    
    
bin 6 und weiter    =MITTELWERT(D5:D6)
'''

def pi_cal():
    counter = 0
    for i in range(len(df['P'])):
        if counter == 0:
            if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                df.at[counter, '(Pi-1+Pi)/2'] = 0
            else:
                pass
        else:
            mean_value = [df.at[counter - 1, 'P'], df.at[counter, 'P']]
            df.at[counter, '(Pi-1+Pi)/2'] = np.mean(mean_value)
            #print(mean_value)
            
            if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                df.at[counter, '(Pi-1+Pi)/2'] = 0
        
        #print("Counter: ", counter)
        #print(df.at[counter, 'V'])
        #print()
        counter += 1

'''
f:
bin 5    =WEIBULL('calculation AEP'!B5 ; 'input+filter'!$B$8 ; 'input+filter'!$B$7 ; WAHR) - WEIBULL('calculation AEP'!B4;'input+filter'!$B$8;'input+filter'!$B$7;WAHR)
                    3,13               ;   weibull_b = 2     ; weibull_a = 9,1232  ; True -             2,63             ;  weibull_b = 2    ; weibull_a = 9,1323; True 
bin 6 und weiter    =WEIBULL('calculation AEP'!B6;'input+filter'!$B$8;'input+filter'!$B$7;WAHR)-WEIBULL('calculation AEP'!B5;'input+filter'!$B$8;'input+filter'!$B$7;WAHR)
'''

def verteilung():
    counter = 0
    a = fk.weibull_a
    b = fk.weibull_b
    
    for value in range(len(df['V'])):
        if counter == 0:
            if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                df.at[counter, 'f'] = 0
            else:
                pass        
        else:
            x = df.at[counter - 1, 'V']
            y = df.at[counter, 'V']
            if x < 0 or y < 0:
                erg = 0
            else:
                val = 1 - np.e ** (-(x / a) ** b)
                val2 = 1 - np.e ** (-(y / a) ** b)
                
                if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                    erg = 0
                else:
                    erg = val2 - val

        #print()
        #print("ID: ", df.at[counter, 'Identifier'])
        #print("BIN: ", df.at[counter, 'Bin'])
        #print("Counter - 1: ", x)
        #print("Counter: ", y)
        #print("val = ", val)
        #print("val2 = ", val2)
        #print("erg = ", erg)
        #print()
            df.at[counter, 'f'] = erg
        counter += 1




rower()
df = df.reset_index(drop=True)

cacu()
pi_cal()
verteilung()



print(df)
print("INDEX: ", df.index)



'''
def f_calculate():
    counter = 1
    for value in range(1, len(df['V'])):
        min_a = weibull_min.pdf(df.at[counter - 1, 'V'], fk.weibull_b, fk.weibull_a)
        min_b = weibull_min.pdf(df.at[counter, 'V'], fk.weibull_b, fk.weibull_a)
        print("min a: ", min_a)
        print("min b: ", min_b)
        print("MIN WEIBULL ERG: ", min_b - min_a)
        print()
        
        max_a = weibull_max.pdf(df.at[counter - 1, 'V'], fk.weibull_b, fk.weibull_a)
        max_b = weibull_max.pdf(df.at[counter, 'V'], fk.weibull_b, fk.weibull_a)
        print("max a: ", max_a)
        print("max b: ", max_b)
        print("MAX WEIBULL ERG: ", max_b - max_a)
        print()
        counter += 1


def f_weibull():
    counter = 1
    for value in range(1, len(df['V'])):
        a = (fk.weibull_b / fk.weibull_a) * (df.at[counter - 1, 'V'] / fk.weibull_a) ** (fk.weibull_b - 1) * np.exp( -(df.at[counter - 1, 'V'] / fk.weibull_a) ** fk.weibull_b)
        b = (fk.weibull_b / fk.weibull_a) * (df.at[counter, 'V'] / fk.weibull_a) ** (fk.weibull_b - 1) * np.exp( -(df.at[counter, 'V'] / fk.weibull_a) ** fk.weibull_b)
        df.at[counter, 'f'] = a - b
        print("F: ", df.at[counter, 'f'])
        counter += 1

def weibull():
    counter = 1
    a = fk.weibull_b
    b = fk.weibull_a
    for value in range(1, len(df['V'])):
            x = df.at[counter - 1, 'V']
            y = df.at[counter, 'V']
            if x < 0 or y < 0:
                erg_1 = 0
                erg_2 = 0
            else:
                # scale = 9.31
                # shape = 2
                print()
                print("ID: ", df.at[counter, 'Identifier'])
                print("BIN: ", df.at[counter, 'Bin'])
                print("Counter - 1: ", x)
                print("Counter: ", y)
                erg_1 = (a / (b ** a)) * (x ** (a - 1)) * (math.e * (-(x / b) ** x))
                erg_2 = (a / (b ** a)) * (y ** (a - 1)) * (math.e * (-(y / b) ** y))
                print("erg2: ", erg_2)
                print("erg1: ", erg_1)
                
                print("erg_2 - erg_1: ", erg_2 - erg_1)
                print("erg_1 - erg_2: ", erg_1 - erg_2)

                erg5 = (a / (b ** a)) * (x ** (a - 1)) * np.e ** (-(x / b) ** a)
                erg6 = (a / (b ** a)) * (y **(a-1)) * np.e ** (-(x / b) ** a)

                print("erg5: ", erg5)
                print("erg6: ", erg6)
                print("erg5 - erg6: ", erg5 - erg6)
                print("erg6 - erg5: ", erg6 - erg5)

                abc = ((a * (x ** (a - 1))) / (b ** a)) * np.e ** (-(x / b)**a)
                cde = ((a * (y ** (a - 1))) / (b ** a)) * np.e ** (-(y / b)**a)
                print("ABF: ", abc)
                print("CDE: ", cde)
                print("EROA: ", abc - cde)
                print("ERAO: ", cde - abc)


                val = (a / b) * (x / b) ** (a-1) * np.e*(-(x / b)**a)
                val1 = (a / b) * (y / b) ** (a-1) * np.e*(-(y / b)**a)
                print("val: ", val)
                print("val1: ", val1)
                print("val - val1: ", val - val1)
                print("val1 - val: ", val1 - val)

                oc = exponweib.stats(x, a, b)
                ac = exponweib.stats(y, a, b)
                print("OC: ", oc)
                print("AC: ", ac)
                #print("OAC: ", oc - ac)
                #print("AOC: ", ac - oc)

                ray = x **((-x**2)/2)
                ray1 = y **((-x**2) / 2)
                ray_erg = ray - ray1
                ray_erg = ray1 - ray
                print("ray: ", ray)
                print("ray1: ", ray1)
                print("ray_erg = ray - ray1: ", ray - ray1)
                print("ray_erg = ray1 - ray: ", ray1 - ray)

            
            #df.at[counter, 'f'] = erg
            
            print()

            

            

            counter += 1

def vert_funk():
    counter = 1
    a = fk.weibull_b
    b = fk.weibull_a
    for value in range(1, len(df['V'])):
        x = df.at[counter - 1, 'V']
        y = df.at[counter, 'V']
        if x < 0 or y < 0:
            erg1 = 0
            erg2 = 0
        else:
            erg1 = 1 - (math.e * ((x / a) ** b))
            print()
            print("ID: ", df.at[counter, 'Identifier'])
            print("BIN: ", df.at[counter, 'Bin'])
            print("Counter - 1: ", x)
            print("Counter: ", y)
            print("erg1: ", erg1)
            erg2 = 1 - (math.e * ((x / b) ** a))
            print("erg2: ", erg2)
        erg = erg2 - erg1
        erg3 = erg1 - erg2
        print("erg: ", erg)
        print("erg3: ", erg3)
        print()
        counter += 1


def row_add():
    counter = 1
    for i in range(len(df['Identifier'])):
        print("ID: ", df.at[counter - 1, 'Identifier'])
        print("counter: ", df.at[counter, 'Identifier'])
        if df.at[counter, 'Identifier'] != df.at[counter - 1, 'Identifier']:

            print("df.at[counter - 1, 'Identifier'].index old: ", df.at[counter - 1, 'Identifier'].index)
            df.at[counter - 1, 'Identifier'].index += 1
            print("df.at[counter - 1, 'Identifier'].index new: ", df.at[counter - 1, 'Identifier'].index)
        counter += 1

'''