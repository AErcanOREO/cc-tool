# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 19:13:02 2022

@author: arda.ercan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime
import os.path

# Name of the csv-file that should be used for the powercurve analysis (Should be in the folder rawdata)
sourceName = '.csv' # This file will be corrected and filter


# Read Data
data = pd.read_csv('./rawdata/' + sourceName , sep=";", skiprows = None)
# Add Datum and zeit to DateTime
data['DateTime'] = pd.to_datetime(data['Datum (Anlage)'] + ' ' + data['Zeit (Anlage)'])
# Delete Datum and Zeit
data = data.drop(['Datum (Anlage)', 'Zeit (Anlage)'], axis = 1)
# Read Pickle File
powerunits = pd.read_pickle('./powerunits.pkl')


# Change Identifier Name
data = data.rename(columns = {'Identifier (Anlage)': 'Identifier'})

# Disabling/anabling additional functions
exportData = True
debugModus = True


# Export data
'''
date = datetime.now().strftime("%Y%m%d")
my_exportFile = "./export/" + date + p + ".csv"
vers = 0
while os.path.isfile(my_exportFile):
    vers = vers + 1
    my_exportFile = "./export/" + date + p + "(" + str(vers) + ")" + ".csv"
data_p.to_csv(my_exportFile, sep=',', decimal='.')
'''






'''
Ablauf:	
1. Dateninput und Setzen der Filter im Blatt "input+filter"		
2. Datenfilterung und Binanalyse im Blatt "filtered data + bin averaging"		
3. Ergebnisdarstellung in Bezug auf die Leistungskennlinie und WEA-Steuerung in den nächsten 4 Blättern		
4. Berechnung des AEP und Aufbereitung der garantierten Leistungskennlinie		
5. Ergebnis in Bezug auf den AEP		
'''

'''
### Excel ###
=Wenn(Condition; True-Condition; False-Condition)

### Python ###
if condition:
    True-Condition
elif:
    False-Condition
'''


############################## Input + Filter ##############################
'''
### Constant Values For each Park ###
Rotordurchmesser = 152 m
Nabenhöhe = 106 m
Abschaltgeschwindigkeit = 30 m/s
Reference Air Density = 1.225 kg/m^3

## Referenzwindgeschwindkeitsverteilung ##
Weibull A = 9.591 m/s
Weibull k = 2.000
V-Mittel = 8.500 m/s


Anlagen:
### Merkur ###
Rotordurchmesser =  m
Nabenhöhe = 102 m
Abschaltgeschwindigkeit =  m/s

### TWB II ###
Rotordurchmesser = 152 m
Nabenhöhe = 106 m
Abschaltgeschwindigkeit = 30 m/s

### Alpha Ventus Senvion ###
Rotordurchmesser = 126 m
Nabenhöhe = 92 m
Abschaltgeschwindigkeit =  m/s

### Alpha Ventus Adwen ###
Rotordurchmesser = 116 m
Nabenhöhe = 90 m
Abschaltgeschwindigkeit =  m/s


### Riffgat ###
Rotordurchmesser =  m
Nabenhöhe = 90 m
Abschaltgeschwindigkeit =  m/s
'''


'''
###### Dictionary ######
B1 = Rotordurchmesser (constant)
B4 = Reference Air Density (constant)
C = Wind Speed (avg)
D = Rotor Speed (avg)
E = Active Power (avg)
I = T Outside Nacelle Level (avg)
J = Pitch Angle (avg)
K = Air Pressure
L = Relative Humidity
M = Air Density
N = Density Corrected Wind Speed
S6 = Lower Limit Rotor Speed (constant)
S10 = Filter (non-) active
T6-T9 = Active Power (constant)
T10 = Filter (non-) active
U6-U9 = Upper Limit Pitch Angle (constant)
'''


'''
### Air Density  ###  [IEC 61400-12-1, eq. 12]
I = T Outside Nacelle Level (avg)
K = Air Pressure
L = Relative Humidity

=WENN(I13 <> ""  ;  1 / (I13 + 273,15) * (K13 * 100 / 287,05 - L13 / 100 * 0,0000205 * EXP(0,0631846 * (I13 + 273,15)) * (1 / 287,05-1 / 461,5)) ; "")
if i13 != 0:
    1 / (I13 + 273,15) * (K13 * 100 / 287,05 - L13 / 100 * 0,0000205 * EXP(0,0631846 * (I13 + 273,15)) * (1 / 287,05-1 / 461,5))


def fAirDensity(data, ):
    
'''

'''
### Density Corrected Wind Speed  ### [IEC 61400-12-1, eq. 14]
C = Wind Speed (avg)
M = Air Density
B4 = Reference Air Density (constant)
  

=WENN(C13 <> ""  ;  C13 * (M13 / $B$4) ^ (1 / 3)  ;  "")

if c13 != 0:
    C13 * (M13 / $B$4) ^ (1 / 3)
'''


'''
### Power Coefficient ### [IEC 61400-12-1, eq. 20]
C = Wind Speed (avg)
E = Active Power (avg)
B1 = Rotordurchmesser (constant)
M = Air Density

=WENN(C13 <> ""  ;  E13 * 1000 / (0,5 * M13 * PI() * ($B$1 / 2) ^ 2 * C13 ^ 3)  ;  "")
if c13 != 0:
    E13 * 1000 / (0,5 * M13 * PI() * ($B$1 / 2) ^ 2 * C13 ^ 3)
'''


'''
### Bin Nummer ###
N = Density Corrected Wind Speed

=WENN(N13 = ""  ;  ""  ;  2 + GANZZAHL((N13 - 0,25) / 0,5))
'''

'''
### Filter ###
### Rotor Speed (avg) ###
D = Rotor Speed (avg)
S10 = Filter (non-)active
S6 = lower Limit Rotor Speed (constant)

=WENN(D13 = ""  ;  ""  ;
      WENN($S$10 = ""  ;  1  ;
           WENN(D13 >= $S$6  ;  1  ;  0)))
'''

'''
### Filter ###
### No Curtailment ###
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
'''




############################## Filtered Data + Bin Averaging ##############################
'''
Row Values (A-P)
=WENN('input+filter'!A13 = ""  ;  #NV  ;  WENN(PRODUKT('input+filter'!$S13:$T13) = 1  ;  'input+filter'!A13  ;  #NV))
'''


'''
### V [m/s] - [IEC 61400-12-1, eq. 15] ###
P = Bin
N = Density Corrected (input + filter)
T = Bin

=MITTELWERTWENN($P$12:$P$52715  ;  T$1  ;  $N$12:$N$52715)
'''

'''
### P [kW] - [IEC 61400-12-1, eq. 16] ###

=MITTELWERT(T12:T52715)
'''

'''
### n ###

=ANZAHL(T12:T52715)
'''

'''
### P max [kW] ###

=MAX(T12:T52715)
'''

'''
### P min [kW] ###

=MIN(T12:T52715)
'''

'''
P std [kW] - [Berechnung auf Basis Stichprobe, IEC61400-12-1, eq. E.9:]

=STABW(T12:T52715)
'''

'''
P std/sqrt(n) [kW] - [statistische Unsicherheit des Binmittels, IEC61400-12-1, eq. E.10]

=T7/WURZEL(T4)
'''
############################## Result Bin Averaged Power Curve ##############################




############################## Calculation AEP ##############################



############################## Garantierte Leistungskennlinie ##############################


