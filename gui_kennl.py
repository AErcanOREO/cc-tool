# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:38:24 2022

@author: arda.ercan
"""
import pandas as pd
from tkinter import *
import tkinter as tk
#import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

# from filter_kennl import *




'''
### Dictionary ###
tk = tkinter
rotor_diameter = Rotordurchmesser
hub_height = Nabenhöhe
ags = Abschaltgeschwindigkeit
mrk = Merkur
twb = TWB II
avs = Alpha Ventus Senvion
ava = Alpha Ventus Adwen
rg = Rifgat
'''

root = tk.Tk()
root.title("Kennlinientool")

# Größe des Fensters entweder mit geometry oder mit tk.Canvas einstellbar
# root.geometry("250x100")

canvas = tk.Canvas(root, width = 270, height = 100) # width 250, height 100
canvas.grid(columnspan = 3, rowspan = 3)

# min size of the root page
root.minsize(width = 200, height = 100)


# Logo
logo = Image.open('omexom_logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column = 0, row = 0)


# Instructions
instructions = tk.Label(root, text = "Wählen Sie ein Anlagentyp aus")
instructions.grid(columnspan = 1, column = 0, row = 1)

# wird ausgeführt, sobald der User einen Anlagentypen ausgewählt hat
def select_csv(button_id):
    select_wea(button_id)
    file = askopenfile(parent = root, mode ='rb', title = "Wählen Sie eine CSV-Datei aus", filetype = [("csv file", "*.csv")])
    df = pd.read_csv(file, sep = ',', skiprows = None)
    print(df)
    check_csv(button_id, file)
    if file:
        reset_wea(button_id)
        print("Die CSV wurde gewählt")
    else:
        reset_wea(button_id)
        

def select_wea(button_id):
    if button_id == 1:
        mrk_text.set("Wähle CSV")
        rotor_diameter = 0
        hub_height = 102
        ags = 0
        print("Rotordurchmesser: ", rotor_diameter , "m", "\nNabenhöhe: ", hub_height, "m",  "\nAbschaltgeschwindigkeit: ", ags, "m/s")
        
    elif button_id == 2:
        twb_text.set("Wähle CSV")
        rotor_diameter = 152
        hub_height = 106
        ags = 30
        print("Rotordurchmesser: ", rotor_diameter , "m", "\nNabenhöhe: ", hub_height, "m",  "\nAbschaltgeschwindigkeit: ", ags, "m/s")
        
    elif button_id == 3:
        avs_text.set("Wähle CSV")
        rotor_diameter = 126
        hub_height = 92
        ags = 0
        print("Rotordurchmesser: ", rotor_diameter , "m", "\nNabenhöhe: ", hub_height, "m",  "\nAbschaltgeschwindigkeit: ", ags, "m/s")
        
    elif button_id == 4:
        ava_text.set("Wählen CSV")
        rotor_diameter = 116
        hub_height = 90
        ags = 0
        print("Rotordurchmesser: ", rotor_diameter , "m", "\nNabenhöhe: ", hub_height, "m",  "\nAbschaltgeschwindigkeit: ", ags, "m/s")
        
    elif button_id == 5:
        rg_text.set("Wähle CSV")
        rotor_diameter = 120
        hub_height = 90
        ags = 0
        print("Rotordurchmesser: ", rotor_diameter , "m", "\nNabenhöhe: ", hub_height, "m",  "\nAbschaltgeschwindigkeit: ", ags, "m/s")

# überprüft ob die eingelesene CSV-Datei mit dem bestätigten Anlagetyp übereinstimmt
'''
DIESE METHODE FUNKTIONIERT NOCH NICHT
'''
def check_csv(button_id, file):
    if button_id == 1 and "mrk" in file:
        print("MRK CHECK DONE")
        
    elif button_id == 2 and "twb" in file :
        print("TWB CHECK DONE!")

    elif button_id == 3 and "avs" in file:
        print("AVS CHECK DONE")
        
    elif button_id == 4 and "ava" in file:
        print("AVA CHECK DONE")

    elif button_id == 5 and "rfg" in file:
        print("RFG CHECK DONE")
    else:
        print("CHECK FAILED!")


# setzt die Button-Texte zurück
def reset_wea(button_id):
    if button_id == 1:
        mrk_text.set("Merkur")
        
    elif button_id == 2:
        twb_text.set("TWB")

    elif button_id == 3:
        avs_text.set("Alpha Ventus Senvion")

    elif button_id == 4:
        ava_text.set("Alpha Ventus Adwen")

    elif button_id == 5:
        rg_text.set("Riffgat")
        


# zeigt Informationen zu den Anlagentypen
def show_info():
    info = tk.Tk()
    info.title("Informationen zu den Anlagen")
    canv = tk.Canvas(info, width = 150, height = 0)
    canv.grid()
    
    mrk_info = tk.Label(info, text = "Merkur:\nRotordurchmesser: LEER m \nNabenhöhe: 102 m \nAbschaltgeschwindigkeit: LEER m/s\n")
    mrk_info.grid()
    
    twb_info = tk.Label(info, text = "TWB II:\nRotordurchmesser: 152 m \nNabenhöhe: 106 m \nAbschaltgeschwindigkeit: 30 m/s\n")
    twb_info.grid()
    
    avs_info = tk.Label(info, text = "Alpha Ventus Senvion:\nRotordurchmesser: 126 m \nNabenhöhe: 92 m \nAbschaltgeschwindigkeit: LEER m/s\n")
    avs_info.grid()
    
    ava_info = tk.Label(info, text = "Alpha Ventus Adwen:\nRotordurchmesser: 116 m \nNabenhöhe: 90 m \nAbschaltgeschwindigkeit: LEER m/s\n")
    ava_info.grid()
    
    rg_info = tk.Label(info, text = "Riffgat:\nRotordurchmesser: LEER m \nNabenhöhe: 90 m \nAbschaltgeschwindigkeit: LEER m/s\n")
    rg_info.grid()
    
    ok_btn = tk.Button(info, command = lambda : close(info), text = "Ok", width = 10, height = 1)
    ok_btn.grid()

# schließt das ausgewählte Fenster
def close(window):
    window.destroy()

# hier wird überprüft welcher Button geklickt wurde
def check_btn(button_id):
    if button_id == 1:
        print()
        
    elif button_id == 2:
        print()

    elif button_id == 3:
        print()
        
    elif button_id == 4:
        print()

    elif button_id == 5:
        print()
        

# Info Button
info_text = tk.StringVar()
info_text.set("Anlagen Infos")
info_btn = tk.Button(root, command = lambda : show_info(), textvariable = info_text, width = 10, height = 1)
info_btn.grid(pady = 20)

# Merkur Button
mrk_text = tk.StringVar()
mrk_text.set("Merkur")
mrk_btn = tk.Button(root, command = lambda : select_csv(1), textvariable = mrk_text, width = 20, height = 3)
mrk_btn.grid()

# TWB II Button
twb_text = tk.StringVar()
twb_text.set("TWB II")
twb_btn = tk.Button(root, command = lambda : select_csv(2), textvariable = twb_text, width=20, height = 3)
twb_btn.grid()

# Alpha Ventus Senvion Button
avs_text = tk.StringVar()
avs_text.set("Alpha Ventus Senvion")
avs_btn = tk.Button(root, command = lambda : select_csv(3), textvariable = avs_text, width = 20, height = 3)
avs_btn.grid()

# Alpha Ventus Adwen Button
ava_text = tk.StringVar()
ava_text.set("Alpha Ventus Adwen")
ava_btn = tk.Button(root, command = lambda : select_csv(4), textvariable = ava_text, width = 20, height = 3)
ava_btn.grid()

# Riffgat Button
rg_text = tk.StringVar()
rg_text.set("Riffgat")
rg_btn = tk.Button(root, command = lambda : select_csv(5), textvariable = rg_text, width = 20, height = 3)
rg_btn.grid()



root.mainloop()
