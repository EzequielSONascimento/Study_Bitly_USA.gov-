# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:15:11 2023

@author: Ezequiel Santana
"""

path = "C:/Users/Ezequiel Santana/Desktop/Ezequiel2023/DATASETWESM/USA_gov.txt"
open(path).readline()

import json   #MODULO JSON PARA LER A STRING JSON E CONVERTE-LA EM UM OBJETO DICIONARIO PYTHON
path = "C:/Users/Ezequiel Santana/Desktop/Ezequiel2023/DATASETWESM/USA_gov.txt"
records = [json.loads(line) for line in open(path)] # O RESULTADO É UMA LISTA DE DICIONARIOS #EX: type(records) -> Out[140]: list / type(records[1]) -> Out[141]: dict

records[0]

#Contando o número de fusos horários:

timezones = [] #criando uma lista de fusos horários

for rec in records:   #para cada dicionario dentro da lista records eu vou procurar o indicie Tz e add dentro de uma nova lista chamada timezone
    if "tz" in rec:
        print(rec["tz"])
        timezones.append(rec["tz"])

timezones[:10] #observando os 10 primeros fusos horários , vemos que alguns estão fazios 

#Contando fusos horários com pandas

import pandas as pd

frame = pd.DataFrame(records)
tz_counts = frame["tz"].value_counts() # O value counts conta com qual frequencia "quantas vezes um indicie aparece em uma lista

#Acertando dados vazios e ausentes

clean_tz = frame["tz"].fillna("Missing")
clean_tz[clean_tz == ""] = "Unknown"

tz_counts = clean_tz.value_counts() 

#Vizualização

import seaborn as sns
subset = tz_counts[:10]
sns.barplot(y = subset.index , x = subset.values)

###############################################################################

results = pd.Series([x.split()[0] for x in frame.a.dropna()]) #retirando informasões da String na coluna a 
results.value_counts()[:8]

#vamos decompor os princípais fusos horários em usarios de windows ou não

import numpy as np

cframe = frame[frame.a.notnull()]


cframe["os"] = np.where(cframe['a'].str.contains("Windows"),"windows","Not Windows")

#agrupando as colunas de fusos horários e usuários de windows 

by_tz_os = cframe.groupby(["tz","os"])

agg_counts = by_tz_os.size().unstack().fillna(0)

count_subset = agg_counts.sum(1).nlargest(10)

#exportando arquivo para CSV

agg_counts.to_csv("Final_frame.csv")