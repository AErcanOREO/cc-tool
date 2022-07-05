# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 14:13:02 2022

@author: arda.ercan
"""

from ast import Index
from cmath import nan
from distutils.log import warn
import telnetlib
from tracemalloc import start
from unittest import skip
import pandas as pd
#from tqdm import tqdm
import filter_export as fk
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

data_mwh = {'Identifier':[],
            'AEP':[],
            'AEP extrapolated':[],
            'Abweichung':[]}


df = pd.DataFrame(data)
df['Bin'] = ba.df_f['BIN']
df['Identifier'] = ba.df_f['Identifier']
df['V'] = ba.df_f['V']
df['P'] = ba.df_f['P']

mwh_df = pd.DataFrame(data_mwh)


def rower():
    global df
    df = df.sort_values(['Identifier', 'Bin', 'V'])
    hk_df = df[df['Identifier'] != 'HK']
    id_df = hk_df.drop_duplicates('Identifier')
    counter = 0

    for i in id_df['Identifier']:
        df_len = len(hk_df)
        if i == 'HK':
            pass
        else:
            df.at[df_len+counter, 'Identifier'] = i
            df.at[df_len+counter, 'Bin'] = 0
            df.at[df_len+counter, 'P'] = 0
            counter += 1

        #df = pd.concat(row_new)
        #df = df.append(new_row, ignore_index=False)
        
    df = df.drop([df_len+counter-1])
    df = df.sort_values(by=['Identifier', 'Bin', 'P'], ascending = True)


def cacu():
    counter = 0
    for value in df['V']:
        if math.isnan(value):
            erg = df.at[counter + 1, 'V'] - 0.5
            df.at[counter, 'V'] = erg

        counter += 1


'''=SVERWEIS(was Sie nachschlagen möchten;
             wo Sie nachschlagen möchten;
             Spaltennummer im Bereich mit dem Rückgabewert;
             ungefähre oder genaue Entsprechung zurückgeben – angegeben als "1/WAHR" oder "0/FALSCH").
'''


'''
Bin:
'result bin averaged power curve'!$N$2 = MIN(BIN Wert aus bin averaging)

'result bin averaged power curve'!$N$5 = MAX(BIN Wert aus bin averaging)
'result bin averaged power curve'!$A$4:$I$84 = Ganze Tabelle aus bin averaging


bin 6    =SVERWEIS('result bin averaged power curve'!$N$2;'result bin averaged power curve'!$A$4:$I$84;1;FALSCH)

bin 7 und weiter    =MIN(A5+1;SVERWEIS('result bin averaged power curve'!$N$5;'result bin averaged power curve'!$A$4:$I$84;1;FALSCH))
'''

def extend():
    global df
    counter = 0
    df_counter = 0
    df_len = len(df)
    id_df = df.groupby('Identifier')

    for id, wea in id_df:
        for counter in wea:
            if wea.at[counter, 'Bin'] == 0 or df.at[counter, 'Identifier'] == 'HK':
                df.at[counter, 'V extended'] = df.at[counter, 'V']
                df.at[counter, 'f extended'] = df.at[counter, 'f']
            else:
                if df.at[counter, 'Bin'] == df.at[counter + 1, 'Bin'] - 1:
                    print("df.at[counter, 'Bin']: ", df.at[counter, 'Bin'])
                    print("df.at[counter + 1, 'Bin'] - 1: ", df.at[counter + 1, 'Bin'] - 1)
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']

                else:
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']

                    df.at[df_len + df_counter, 'Identifier'] = df.at[counter, 'Identifier']
                    df.at[df_len + df_counter, 'Bin'] = df.at[counter, 'Bin']
                    df.at[df_len + df_counter, 'V'] = df.at[counter, 'V']
                    df.at[df_len + df_counter, 'V extended'] = 30
                    df.at[df_len + df_counter, 'P'] = df.at[counter, 'P']
                    df_counter += 1

def extended():
    global df
    df_len = len(df)
    counter = 0
    df_counter = 1

    for i in range(len(df['Bin'])):
        #print("DF_LEN: ", df_len)
        #print("B: ", b)
        #print("COUNTER: ", counter)
        #print("V: ", df.at[counter, 'V'])
        #print()

        if counter == df_len-1:
            print("FIRST IF")
            print("INDEX: ", df.index[i])
            df.at[counter, 'V extended'] = df.at[counter, 'V']
            df.at[counter, 'f extended'] = df.at[counter, 'f']
            counter -= 1
            df.at[counter+1, 'V extended'] = df.at[counter+1, 'V']


        if df.at[counter, 'Bin'] == 0.0 or df.at[counter, 'Identifier'] == 'HK':
            print("SEC IF ")
            print("INDEX: ", df.index[i])
            df.at[counter, 'V extended'] = df.at[counter, 'V']
            df.at[counter, 'f extended'] = df.at[counter, 'f']

        elif df.at[counter, 'Identifier'] == df.at[counter + 1, 'Identifier']:
            print("ELIF ")
            print("INDEX: ", df.index[i])
            if df.at[counter, 'Bin'] == df.at[counter + 1, 'Bin'] - 1:
                print("ELiF IF IF")
                print("INDEX: ", df.index[i])
                print("df.at[counter, 'Bin']: ", df.at[counter, 'Bin'])
                print("df.at[counter + 1, 'Bin'] - 1: ", df.at[counter + 1, 'Bin'] - 1)
                df.at[counter, 'V extended'] = df.at[counter, 'V']
                df.at[counter, 'f extended'] = df.at[counter, 'f']

            else:
                print("ELSE")
                print("INDEX: ", df.index[i])
                df.at[counter, 'V extended'] = df.at[counter, 'V']
                df.at[counter, 'f extended'] = df.at[counter, 'f']

                df.at[df_len + df_counter, 'Identifier'] = df.at[counter, 'Identifier']
                df.at[df_len + df_counter, 'Bin'] = df.at[counter, 'Bin']
                df.at[df_len + df_counter, 'V'] = df.at[counter, 'V']
                df.at[df_len + df_counter, 'V extended'] = 30
                df.at[df_len + df_counter, 'P'] = df.at[counter, 'P']
                df_counter += 1
        
        

        counter += 1
        
    #df['V extended'] = df['V extended'].fillna(30)
    
    
    df = df.sort_values(['Identifier', 'Bin', 'V'])
    df = df.reset_index(drop=True)
    print(df)

def extendo():
    global df
    df_len = len(df)
    counter = 0
    df_counter = 1

    group_df = df.groupby('Identifier')

    for id, wea in group_df:


        if id == 'HK':
            
            df.at[counter, 'V extended'] = df.at[counter, 'V']
            df.at[counter, 'f extended'] = df.at[counter, 'f']
        
        else:

            for i in range(len(wea)):
                print("COUNTER: ", counter)

                if wea['Bin'].index[counter] == 0.0:
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']

                elif wea.index[counter] == wea.index[-1]:
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']
                    break

                elif wea['Identifier'].index[counter] == wea['Identifier'].index[counter + 1] - 1:
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']
                
                elif counter == len(wea):
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']

                else:
                    df.at[counter, 'V extended'] = df.at[counter, 'V']
                    df.at[counter, 'f extended'] = df.at[counter, 'f']

                    df.at[df_len + df_counter, 'Identifier'] = df.at[counter, 'Identifier']
                    df.at[df_len + df_counter, 'Bin'] = df.at[counter, 'Bin']
                    df.at[df_len + df_counter, 'V'] = df.at[counter, 'V']
                    df.at[df_len + df_counter, 'V extended'] = 30
                    df.at[df_len + df_counter, 'P'] = df.at[counter, 'P']
                    df_counter += 1
        counter += 1

    df = df.sort_values(['Identifier', 'Bin', 'V'])
    df = df.reset_index(drop=True)
    #print(df)
    '''
                if wea['Bin'].index[counter] == 0.0:
                    df['V extended'].index[counter] = df['V'].index[counter]
                    df['f extended'].index[counter] = df['f'].index[counter]

                elif wea.index[counter] == wea.index[-1]:
                    df['V extended'].index[counter] = df['V'].index[counter]
                    df['f extended'].index[counter] = df['f'].index[counter]
                    break

                elif wea['Identifier'].index[counter] == wea['Identifier'].index[counter + 1] - 1:
                    df['V extended'].index[counter] = df['V'].index[counter]
                    df['f extended'].index[counter] = df['f'].index[counter]
                
                elif counter == len(wea):
                    df['V extended'].index[counter] = df['V'].index[counter]
                    df['f extended'].index[counter] = df['f'].index[counter]

                else:
                    df['V extended'].index[counter] = df['V'].index[counter]
                    df['f extended'].index[counter] = df['f'].index[counter]

                    df['Identifier'].index[df_len + df_counter] = df['Identifier'].index[counter]
                    df['Bin'].index[df_len + df_counter] = df['Bin'].index[counter]
                    df['V'].index[df_len + df_counter] = df['V'].index[counter]
                    df['V extended'].index[df_len + df_counter] = 30
                    df['P'].index[df_len + df_counter] = df['P'].index[counter]
                    df_counter += 1'''

def delete_row():
    global df
    counter = 1
    df = df.reset_index(drop=True)
    group_df = df.groupby('Identifier')
    for id, wea in group_df:
        #df = df.reset_index(drop=True)
        #wea = wea.reset_index(drop=True)
        
        #print("COUNTER: ", counter)
        if id != 'HK':
            wea['Doppel'] = wea.duplicated(subset='Bin', keep='first')
            print(wea['Doppel'])
            for counter in range(len(wea['Doppel'])):
                #print("VALUE: ", counter)
                if wea.at[counter, 'Doppel'] == True:
                    #print("wea.at[counter, 'Doppel']: ", wea.at[counter, 'Doppel'])

                    #print("wea.index[counter] = ", wea.index[counter])
                    #print("wea.index[counter + 1] = ", wea.index[counter + 1])
                    #print("wea.index[-1] = ", wea.index[-1])
                    counter = wea.index[-1] + 1
                    #df = df.drop([counter+1, wea.index[-1]])
                    #wea = wea.drop([counter+1, wea.index[-1]])
                    #wea = wea.reset_index(drop=True)
                    break

                counter += 1
        #print("WEA")
        #print(wea)


def del_row():
    global df
    counter = 0
    start_list = []
    end_list = []
    df = df.reset_index(drop=True)
    group_df = df.groupby('Identifier')
    for id, wea in group_df:
        if id != 'HK':
            wea['Doppel'] = wea.duplicated(subset='Bin', keep='first')
            #print(wea)
            for boolean in wea['Doppel']:
                #print("BOOLEAN VALUE: ")
                #print(boolean)
                if boolean == True:
                    idx_true = wea[wea['Doppel'] == True].index + 1
                    end_df = wea.index[-1]

                    start_df = idx_true[0]

                    #wea.at[start_df - 1, 'Doppel'] = False

                    for i in wea:
                        if start_df <= end_df:
                            df.at[start_df, 'Doppel'] = True
                            wea.at[start_df, 'Doppel'] = True

                            start_df += 1
                        else:
                            df.drop(df[df['Doppel'] == True].index, inplace=True)
                            #print("DAS IST TRUE WEA")
                            #print(wea)
                            break
    
                    '''
                    
                    start_list.append(idx_true[0])
                    end_list.append(end_df)


                    print("idx_true = ", idx_true[0])
                    print("end_df = ", end_df)

                    print("Start List : ", start_list)
                    print("End List: ", end_list)
                    
                
                    #wea[:idx_true]
                    #wea.iloc[:idx_true[0]]
                    print(wea)
                    print("ID: ", id)
                    

                    #wea = wea.drop([idx_true, end_df])
                    #df = df.drop([idx_true, end_df])
                    
                    break
                '''
                counter += 1
        else:
            pass
    
    df = df.reset_index(drop=True)
    print("DAS IST UPDATE DF: ")
    print(df)
    

    '''
    distance = 0

    print("LÄNGE: ", len(start_list))

    for list_counter in range(0, len(start_list)):
        df.drop(df.index[(start_list[list_counter] - distance) : (end_list[list_counter] + 1 - distance)], inplace = True)
        distance = end_list[list_counter] - start_list[list_counter]
        df = df.reset_index(inplace=True)

        #df = df.drop(df.iloc[start_list[list_counter] : (end_list[list_counter]+1)])
        print("List Counter: ", list_counter)
        print("START LIST: ", start_list)
        print("END LIST: ", end_list)

    #

    #print("List Counter ENDE: ", list_counter)
    #print("START LIST: ", start_list)
    #print("END LIST: ", end_list)
        

    #df['Doppel'] = df.duplicated(subset='Bin', keep='first')
    #print("DAS IST DF LO")
    #print(df)
    #for i in df:
    #    if df.at[counter, 'Identifier'] != 'HK':
    #       
    #        if df.at[counter, 'Identifier'] == df.at[counter + 1, 'Identifier']:
    #            if df.at[counter, 'Bin'] == df.at[counter + 1, 'Bin']:
    #                if df.at[counter, 'Identifier'] == df.at[counter + 2, 'Identifier']:
    #                    #df = df.drop(counter+2)
    #                    print("HALLLOOO")
        
    #    counter += 1
    '''

def delete_extended():
    global df
    counter = 0
    df = df.reset_index(drop=True)
    group_df = df.groupby('Identifier')
    for id, wea in group_df:
        if id != 'HK':
            wea['Doppel'] = wea.duplicated(subset='Bin', keep='first')
            print(wea)
            print(wea['Doppel'])
            if wea['Doppel'].isin(True):
                idx_true = wea[wea['Doppel']==True].index[0]
                print("idx_true,", idx_true)
            #for boolean in wea['Doppel']:
             #   print("BOOLEAN: ", boolean)
              #  true_counter = 0
               # if boolean == True:
                #    idx_true = wea[wea['Doppel']==True].index[0]
                 #   print("id_true,", idx_true)
                  #  print("wea.index[-1], ", wea.index[-1])
                   # true_counter += 1
                    #print("wea[1]: ",wea.at[counter-1, 'Bin'])
                    #print("wea[2]: ", wea.at[counter, 'Bin'])
                #if true_counter == 1:
                 #   wea = wea.drop([idx_true +1, wea.index[-1]])
                  #  df = df.drop([idx_true +1, wea.index[-1]])
                   # break
                counter += 1
            print("WEA UPDATE")
            print(wea)
        #if True in wea['Doppel']:
        #    print("TRUE IN WEA")
          #  id_true = wea[wea['Doppel'] == True].index[0]
            #print("ID", id_true.values)
            #print("idi: ", idi)
            #print("Len wea: ", len(wea))
            #print("I in range: ", idi+1)
            #print("BIN: ", wea.at[idi, 'Bin'])
            #print("wea.index[-1]: ", wea.index[-1])
         #   df = df.drop([id_true +1, wea.index[-1]])
            #print("gedroppter df", df)

    df = df.reset_index(drop=True)


'''
(Pi-1+pi)/2:
    
bin 5    =MITTELWERT(D4:D5)    
    
bin 6 und weiter    =MITTELWERT(D5:D6)
'''

def pi_cal():
    counter = 0

    for i in range(len(df)):
        if counter == len(df) - 1:
            mean_value = [df.at[counter - 1, 'P'], df.at[counter, 'P']]
            df.at[counter, '(Pi-1+Pi)/2'] = np.mean(mean_value)
            
            counter -=1

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
    
    for i in range(len(df)):
        #print("Counter VERTEILUNG: ", counter)

        if counter == 0:
            if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                df.at[counter, 'f'] = 0
            else:
                pass
        elif counter == len(df) - 1:
            
            x = df.at[len(df)-2, 'V']     
            y = df.at[len(df)-1, 'V']


            val = 1 - np.e ** (-(x / a) ** b)
            val2 = 1 - np.e ** (-(y / a) ** b)

            
            erg = val2 - val
            df.at[counter, 'f'] = erg
            counter -= 1
            
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

            df.at[counter, 'f'] = erg
        counter += 1


def extend_verteilung():
    counter = 0
    a = fk.weibull_a
    b = fk.weibull_b
    
    for i in range(len(df['V'])):
        if counter == 0:
            if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                df.at[counter, 'f extended'] = 0
            else:
                pass
        elif counter == len(df) - 1:
            
            x = df.at[len(df)-2, 'V extended']     
            y = df.at[len(df)-1, 'V extended']


            val = 1 - np.e ** (-(x / a) ** b)
            val2 = 1 - np.e ** (-(y / a) ** b)

            erg = val2 - val
            df.at[counter, 'f extended'] = erg
            counter -= 1
        else:
            x = df.at[counter - 1, 'V extended']
            y = df.at[counter, 'V extended']

            if x < 0 or y < 0:
                erg = 0
            else:
                val = 1 - np.e ** (-(x / a) ** b)
                val2 = 1 - np.e ** (-(y / a) ** b)

                if df.at[counter, 'Bin'] == 0 and df.at[counter, 'P'] == 0:
                    erg = 0
                else:
                    erg = val2 - val

            df.at[counter, 'f extended'] = erg

        counter += 1




def mwh_cacu():
    '''
    AEP

    E5-E85 = (Pi-1+Pi)/2

    F5-F85 = f

    =SUMMENPRODUKT($E$5:$E$85;$F$5:$F$85)*8760/1000
    '''
    
    global mwh_df
    df_counter = 0
    id_df = df.groupby('Identifier')
    #print("ID_DF")
    #print(id_df)
    for id, wea in id_df:
        #print("ID")
        #print(id)
        #print(wea.index)
        counter = 0
        
        val = 0
        erg = 0
        wea = wea.reset_index(drop=True)
        #print(wea.index)
        for i in range(wea.index[-1]):
            x = wea.at[counter, '(Pi-1+Pi)/2']
            y = wea.at[counter, 'f']

            val = x * y

            erg += val
            counter += 1
        mwh_df.at[df_counter, 'Identifier'] = id
        mwh_df.at[df_counter, 'AEP'] = erg * 8700 / 1000
        #print("DF_COUNTER: ", df_counter)

        df_counter += 1
        

def mwh_extra_cacu():
    '''
    AEP extrapolated

    E5-E85 = (Pi-1+Pi)/2

    G5-G85 = f extended

    =SUMMENPRODUKT($E$5:$E$85;$G$5:$G$85)*8760/1000
    '''
    
    global mwh_df
    df_counter = 0
    id_df = df.groupby('Identifier')
    for id, wea in id_df:
        counter = 0
        val = 0
        erg = 0
        wea = wea.reset_index(drop=True)
        for i in range(wea.index[-1]):
            x = wea.at[counter, '(Pi-1+Pi)/2']
            y = wea.at[counter, 'f extended']

            val = x * y

            erg += val
            counter += 1
        mwh_df.at[df_counter, 'AEP extrapolated'] = erg * 8700 / 1000
        df_counter += 1


    mwh_df = mwh_df.reset_index(drop=True)

def abweichung():
    '''
    Abweichung

    B = AEP extrapolated

    C = MWH HK

    =(B3-C3)/C3*100
    '''
    global mwh_df
    counter = 0
    for i in range(len(mwh_df)):
        x = mwh_df.at[counter, 'AEP extrapolated']
        y = mwh_df.at[mwh_df.index[-1], 'AEP extrapolated']

        erg = (x-y)/y*100

        mwh_df.at[counter, 'Abweichung'] = erg
        counter += 1


rower()
df = df.reset_index(drop=True)
cacu()
#extendo()
extended()
df['V extended'] = df['V extended'].fillna(30)
del_row()
df = df.drop('Doppel', axis=1)
verteilung()
extend_verteilung()
pi_cal()

print(df)

mwh_cacu()
mwh_extra_cacu()
abweichung()
print(mwh_df)

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



def del_ext():
    global df
    counter = 0
    index_list = []
    group_df = df.groupby('Identifier')
    for id, wea in group_df:
        counter = 0
        #print("ID: ", id)
        #print("WEA: ", wea)
        #print("INDEX: ", group_df.indices)
        #print("WEA ID: ", wea.index[0])
        #print("DUPLICATES: ", wea.duplicated(subset='Bin', keep='first'))
        
        #print("INDEX_LIST: ", index_list)
        #for i in index_list:
         #   print("i: ", i)
        wea['Doppel'] = wea.duplicated(subset='Bin', keep='first')
        print(wea)
        for i in wea['Doppel']:
            print("I: ", i)
            if i == True:
                index_list.append(wea.Index[counter])
            counter += 1

    for b in df['Bin']:
        print("COUNTER: ", counter)
        print("B: ", b)
        print("Bin: ", df.at[counter, 'Bin'])
        print()

        if df.at[counter, 'Identifier'] == df.at[counter + 1, 'Identifier'] and df.at[counter, 'Identifier'] != 'HK':
            if b == df.at[counter + 1, 'Bin']:
                i = counter + 1
            
                for i in df['Identifier']:
                    if i == df.at[counter + 2, 'Identifier']:

                        print("DF DROP: ", df.at[i+1, 'Bin'])
                        df.at[i+1, 'Bin'] = 'DROP'
                        print("df.at[counter, 'Bin']: ", df.at[i+1, 'Bin'])
                        print(df.at[i+1 , 'V'])
                        #df = df.drop(df[counter + 2])
                        #df = df.reset_index(drop=True)
                    else:
                        break

        counter += 1
        #print(df)
    
    print("DEL_ENT AUSGEFÜHRT")
    #wea.drop(wea.index[wea[wea['Doppel'] == True].index + 1 : len(wea)-1])
        #print("WEA DROP TRUE: ", wea)
        #wea = wea.drop(wea[wea['Doppel'] == True].index + 1, len(wea)-1)
        #print("WEA DROP: ", wea)
            




        #len_wea = len(wea)
        #for i in range(len(wea['Doppel'])):
        #    print("I: ", i)
        #    print("COunter: ", counter)


            #print("wea.at[counter, 'Doppel']: ", wea.at[counter, 'Bin'])
            #if True in wea['Doppel']:
            #id_true = wea[wea['Doppel'] == True].index
            #print("ID_TRUE: ", id_true)
            #if wea.at[counter, 'Doppel'] == True:
                #if counter + 1 <= i:
                    #index_list.append(wea.Index[counter + 1])
            #counter += 1
            #print("INDEX_LIST: ", index_list)
    
    # df = df.drop(df[df[df.index] == grouped_df.index])

            #print("ID: ", id)
            #print("WEA: ", wea)
            #print("INDEX: ", group_df.indices)
            #print("WEA ID: ", wea.index[0])
            #print("DUPLICATES: ", wea.duplicated(subset='Bin', keep='first'))
            
            #print("INDEX_LIST: ", index_list)
            #for i in index_list:
            #   print("i: ", i)

'''