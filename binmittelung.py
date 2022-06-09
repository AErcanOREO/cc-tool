import pandas as pd
import datetime
import math
import os.path
from tqdm import tqdm
import filter_kennl_final_2 as fk


print("NEUE DATEI ERREICHT")

print(fk.df)

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

df = pd.DataFrame(data)

twb_kennlinie = [{'Identifier': 'HK', 'V': 3.5, 'P': 5.112170643 },
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
                  {'Identifier': 'HK', 'V': 29, 'P':   6386.350148}]


filtered_fk = fk.df[(fk.df['Lower Limit Filter'] == True) & (fk.df['Active Power Filter'] == True)]

print("Filtered FK:")
print(filtered_fk)

filtered_fk = filtered_fk.sort_values(by=['Identifier', 'Bin'], ascending=True)

print("Sortiert Filtered_FK")
print(filtered_fk)

def calculate_df(dataframe):
    counter = 0
    df_counter = 0
    n = 0
    v = 0
    p = 0
    print(dataframe)
    for i in tqdm(range(0, len(dataframe))):
        if dataframe.at[counter, 'Bin'] == dataframe.at[i, 'Bin']:
            n += 1
            v += dataframe.at[counter, 'Corrected Wind Speed']
            p += dataframe.at[counter, 'Active Power']
        if dataframe.at[counter, 'Bin'] != dataframe.at[i, 'Bin']:
            df.at[df_counter, 'n'] = n
            df.at[df_counter, 'BIN'] = dataframe.at[counter, 'Bin']

            try:
                df.at[df_counter,'V'] = float(v / n)
                df.at[df_counter, 'P'] = float(p / n)
            except:
                continue
            n=0
            v=0
            p=0
            df_counter+=1
        counter += 1


calculate_df(filtered_fk)

print(df)