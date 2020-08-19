# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:12:15 2020

@author: Harshit
"""

from tika import parser
import glob, os
import pandas as pd
from bs4 import BeautifulSoup
import codecs
import re
import numpy as np
import lexnlp.extract.en.entities.nltk_re


def multipdftotxt(path):
    df = pd.DataFrame(columns = ['S.No', 'File_Name', 'Author', 'Creation_Date', 'Title','Content'])
    pdfs = []
    i=0
    os.chdir(path)
    types = ['*.pdf', '*.doc', '*.docx']
    textfiles = []
    
    for typ in types:
        textfiles.append(glob.glob(typ))
    flat_list = []
    for sublist in textfiles:
        for item in sublist:
            flat_list.append(item)
    textfiles = flat_list
        
    for file in textfiles:
        print(file)
        raw = parser.from_file(file)
        
        text = raw['content']
        dict2 = raw['metadata']
        Author = dict2.get('Author')
        Creation_Date = dict2.get('Creation-Date')
        title = dict2.get('title')
        i = i+1
        df1 = {'S.No': i,'File_Name': file,'Author': Author,'Creation_Date': Creation_Date, 'Title': title,'Content': text}
        df = df.append(df1, ignore_index=True)
    df = df.replace('\n', ' \n ', regex=True, ) 
    df = df.replace('\t', ' ', regex=True)
    df = df.dropna(subset=['Content'])
  
    return df

######################################################################################################3

def dftod(df):
    l = []
    for i in df['Content']:
        l.append(i)
    emailname = []
    for i in df['File_Name']:
        emailname.append(i)
    d = dict(zip(emailname, l))

    k = [v.strip() for k,v in d.items()]
    k = [re.sub(' +', ' ', temp) for temp in k]
    k = [re.sub('\n +', '\n', temp) for temp in k]
    k = [re.sub('\n+', '\n', temp) for temp in k] 
    
    d = dict(zip(emailname, k))
    return d



