#### altman z-score calculator

# import libraries

import os
import pandas as pd
import numpy as np
import tkinter
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import yahooquery
from yahooquery import Ticker
from datetime import datetime
from ttkbootstrap.constants import *
from numpy import math
import requests

# dataframe for output file

cols = ['ticker','name', 'z score']
df = pd.DataFrame(columns = cols)

# create query box

root = ttk.Window(themename='litera')
root.title('Altman Z-Score Calculator')

lst_label = ttk.Label(root, text = 'Enter the ticker below.')
lst_label.pack(pady=5)
lst_label_1 = ttk.Label(root, text = 'Must end with ".TO" if TSX-listed.')
lst_label_1.pack(pady=1)

lst_label_2 = ttk.Label(root, text = "")
lst_label_2.pack(anchor='c', padx=50)
lst_label_3 = ttk.Label(root, text = "  Less than 1.8 = Distress Zone")
lst_label_3.pack(anchor='c', padx=50)
lst_label_4 = ttk.Label(root, text = "From 1.8 to 3.0 = Grey Zone")
lst_label_4.pack(anchor='c', padx=50)
lst_label_4 = ttk.Label(root, text = "Greater than 3.0 = Safe Zone")
lst_label_4.pack(anchor='c', padx=50)

entry_lst = ttk.Entry(root)
entry_lst.pack(pady=10,padx=(5,5))

# gather data

def zscore():    
    global df
    global rows
    global name
    global i

    i = entry_lst.get()
    name = Ticker(''+i+'').price.get(''+i+'').get('longName')
    rev = Ticker(''+i+'').get_financial_data('TotalRevenue',frequency='q')['TotalRevenue'][-1]
    ebit = Ticker(''+i+'').get_financial_data('EBIT', frequency='q')['EBIT'][-1]
    tot_a = Ticker(''+i+'').get_financial_data('TotalAssets', frequency = 'q')['TotalAssets'][-1]
    tot_l = Ticker(''+i+'').get_financial_data('TotalLiabilitiesNetMinorityInterest', frequency = 'q')['TotalLiabilitiesNetMinorityInterest'][-1]
    ar = Ticker(''+i+'').get_financial_data('AccountsReceivable', frequency='q')['AccountsReceivable'][-1]
    if isinstance(Ticker(''+i+'').get_financial_data('Inventory',frequency='q')['Inventory'][-1],float) == False:
        inv = 0
    else:
        inv = Ticker(''+i+'').get_financial_data('Inventory',frequency='q')['Inventory'][-1]

    ap = Ticker(''+i+'').get_financial_data('AccountsPayable',frequency='q')['AccountsPayable'][-1]
    re = Ticker(''+i+'').get_financial_data('RetainedEarnings', frequency = 'q')['RetainedEarnings'][-1]
    mc = Ticker(''+i+'').price.get(''+i+'').get('marketCap')

# compute zscore            

    wc = ar + inv + ap
    a = wc / tot_a
    b = re / tot_a
    c = ebit / tot_a
    d = mc / tot_l
    e = rev / tot_a
    z_score = round((1.0*a) + (1.4*b) + (3.3*c) + (0.6*d) + (0.99*e),2)
    rows = {'ticker':i,'name':name,'z score':z_score}
    df = pd.concat([df, pd.DataFrame([rows])])
    if isinstance(z_score,float) == True:
        messagebox.showinfo(message = "z score for "+str(name)+" = "+str(z_score))
    
# export and save ouput

def save_file():
    global file
    file = filedialog.asksaveasfile(mode='w', filetypes = [('Excel Workbook','.xlsx'),('CSV (Comma delimited)', '.csv')], defaultextension = ".xlsx")
    if os.path.splitext(file.name)[-1] == '.xlsx':
        df.to_excel(file.name)
    if os.path.splitext(file.name)[-1] == '.csv':
        df.to_csv(file.name)
    
save = ttk.Button(root, text = 'save', command=save_file, bootstyle='primary', width=8) 
save.pack(pady=10, padx=(10,20),side=RIGHT)

lst_button = ttk.Button(root, text='run', command=zscore, bootstyle='success', width=8)
lst_button.pack(pady=10, padx=10, side=RIGHT)

root.mainloop()