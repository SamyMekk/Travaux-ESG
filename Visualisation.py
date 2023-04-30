# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:06:59 2023

@author: samym
"""
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pyxlsb import open_workbook as open_xlsb
from sklearn.cluster import KMeans



# Fonction de Conversion 
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')



# Imports
EScore=pd.read_excel("data/EnvScore20202022.xlsx",index_col=0)
GScore=pd.read_excel("data/GouvScore20202022.xlsx",index_col=0)
SocialScore=pd.read_excel("data/SocialScore20202022.xlsx",index_col=0)
Score=pd.read_csv("data/Score.csv",index_col=0)
GlobalScore=Score.reindex(index=GScore.index)
Symbols=pd.read_csv("data/symbolsandIndustry.csv",index_col=0)



# Titre : 
    
st.title("Application Simple permettant de visualiser la répartition des notations E,S,G des entreprises du S&P500")


st.subheader("Visualisons rapidement les données :")
st.dataframe(GlobalScore)
ScoreGlobal=convert_df(GlobalScore)
st.download_button("Cliquer sur le bouton si vous enregistez le dataframe complet au format csv",ScoreGlobal, file_name= "GlobalScore.csv")
def user_input():
    option=st.sidebar.selectbox("Quelle Secteur d'Activités des entreprises du S&P 500 voulez-vous regarder ? ",('Information Technology','Industrials','Financials','Consumer Discretionary','Health Care','Consumer Staples','Real Estate','Materials','Energy','Communication Services'))
    return option

SectorActivity=user_input()

def user_input2():
    option=st.sidebar.selectbox("Quelle période voulez-vous visualiser ? ",('Janvier 2020','Février 2020','Mars 2020','Juillet 2020','Août 2020','Octobre 2020','Janvier 2021','Février 2021','Mars 2021','Mai 2021','Septembre 2021','Fevrier 2022','Mai 2022'))
    return option

Time=user_input2()
   
st.header("Voici la partie concernant la visualisation sur tout le dataframe ")

FullData=[]
for date in Score.columns:
    x1=EScore[date].values
    x2=GScore[date].values
    x3=SocialScore[date].values
    A=pd.DataFrame(list(zip(x1,x2,x3)),columns=["Environnement","Gouvernance","Social"])
    FullData.append(A[["Environnement","Gouvernance","Social"]].values)
    
model = KMeans(n_clusters = 3, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0)
FullDataPredict=[]
for i in range(0,13):
    FullDataPredict.append(model.fit_predict(FullData[i]))
    
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Environnemental Score-->')
ax.set_ylabel('Gouvernance Score-->')
ax.set_zlabel('Social Score-->')
ax.legend()

# Design a slider to choose which simulation to show 


DictionnaireValeur={'Janvier 2020':0,'Février 2020' : 1 ,'Mars 2020':2,'Juillet 2020':3,'Août 2020':4,'Octobre 2020':5,'Janvier 2021':6,'Février 2021':7,'Mars 2021':8,'Mai 2021':9,'Septembre 2021':10,'Fevrier 2022':11,'Mai 2022':12}
Number=DictionnaireValeur[Time]
ax.cla()
ax.scatter(FullData[Number][FullDataPredict[Number] == 0,0],FullData[Number][FullDataPredict[Number] == 0,1],FullData[Number][FullDataPredict[Number] == 0,2], s = 40 , color = 'blue', label = "cluster 0")
ax.scatter(FullData[Number][FullDataPredict[Number] == 1,0],FullData[Number][FullDataPredict[Number] == 1,1],FullData[Number][FullDataPredict[Number] == 1,2], s = 40 , color = 'red', label = "cluster 1")
ax.scatter(FullData[Number][FullDataPredict[Number] == 2,0],FullData[Number][FullDataPredict[Number] == 2,1],FullData[Number][FullDataPredict[Number]== 2,2], s = 40 , color = 'yellow', label = "cluster 2")
ax.set_xlabel('Environnemental Score-->')
ax.set_ylabel('Gouvernance Score-->')
ax.set_zlabel('Social Score-->')
ax.set_xlim3d(0, 23)
ax.set_ylim3d(0, 23)
ax.set_zlim3d(0, 23)
plt.title("Clustering  "+str(Time))
st.pyplot(fig)
    

# Partie Sectorielle

st.subheader("Vous avez choisi de prendre  le secteur suivant : " + str(SectorActivity) + " pour la période de " + str(Time))

def get_data_sector(sector):
    "Filter Data set on a given sector"
    W=Symbols[Symbols["GICS Sector"]==sector]["Symbol"].values
    A=[]
    for element in W:
        if element in GlobalScore.index:
            A.append(element)
    return GlobalScore.loc[A],A


data,index=get_data_sector(SectorActivity)
st.subheader("Il contient " + str(len(data)) + " entreprises du S&P 500 ")
st.dataframe(data)


csv = convert_df(data)
st.download_button("Cliquer sur le bouton si vous enregistez la data associée au secteur " +str(SectorActivity) + "  au format csv",csv, file_name= str(SectorActivity) + str(Time) + ".csv")


st.header("Voici la partie concernant la visualisation : ")



M=[]
for date in Score.columns:
    x1=EScore.loc[index][date].values
    x2=GScore.loc[index][date].values
    x3=SocialScore.loc[index][date].values
    A=pd.DataFrame(list(zip(x1,x2,x3)),columns=["Environnement","Gouvernance","Social"])
    M.append(A[["Environnement","Gouvernance","Social"]].values)
    
model = KMeans(n_clusters = 3, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0)
L=[]
for i in range(0,13):
    L.append(model.fit_predict(M[i]))
    
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Environnemental Score-->')
ax.set_ylabel('Gouvernance Score-->')
ax.set_zlabel('Social Score-->')
ax.legend()

# Design a slider to choose which simulation to show 

ax.cla()
ax.scatter(M[Number][L[Number] == 0,0],M[Number][L[Number] == 0,1],M[Number][L[Number] == 0,2], s = 40 , color = 'blue', label = "cluster 0")
ax.scatter(M[Number][L[Number] == 1,0],M[Number][L[Number] == 1,1],M[Number][L[Number] == 1,2], s = 40 , color = 'red', label = "cluster 1")
ax.scatter(M[Number][L[Number] == 2,0],M[Number][L[Number] == 2,1],M[Number][L[Number]== 2,2], s = 40 , color = 'yellow', label = "cluster 2")
ax.set_xlabel('Environnemental Score-->')
ax.set_ylabel('Gouvernance Score-->')
ax.set_zlabel('Social Score-->')
ax.set_xlim3d(0, 23)
ax.set_ylim3d(0, 23)
ax.set_zlim3d(0, 23)
plt.title("Clustering  "+str(Time))
st.pyplot(fig)
    
