# -*- coding: utf-8 -*-
import json
import pandas as pd
import os.path
import numpy as np
import sys
from sklearn.cluster import KMeans 
#import matplotlib.pyplot as plt
#import csv
#import math
current_path = os.path.dirname(__file__)

#return the list of countries
def get_countries():
  europe = list()
  africa =list()
  north_america = list()
  south_america = list()
  asia = list()
  oceania = list()

  data = pd.read_csv(current_path+"/static/countries/countries.csv", sep=";")
  for i, country in data.iterrows():
    if country['continent'] == "AF":
      africa.append([country['name'].strip(), country['iso3']])
    elif country['continent'] == "EU":
      europe.append([country['name'].strip(), country['iso3']])
    elif country['continent'] == "SA":
      south_america.append([country['name'].strip(), country['iso3']])
    elif country['continent'] == "AS":
      asia.append([country['name'].strip(), country['iso3']])
    elif country['continent'] == "OC":
      oceania.append([country['name'].strip(), country['iso3']])
    elif country['continent'] == "AN":
      north_america.append([country['name'].strip(), country['iso3']])
  countries = { "europe": europe, "africa": africa, "north_america": north_america, "south_america": south_america, "asia": asia, "oceania": oceania}
  return countries

#return the ist of features
def get_features():
  data=pd.read_csv(current_path+"/static/factbookpro.csv",sep=';')
  features = list(data.columns.values)
  list_features = list()
  for i, f in enumerate(features):
    if i > 1:
      list_features.append([i,f])
  return list_features





def beautiful_json_cluster(jsM,KC,FT):
  clusters = dict()
  countries_array = json.loads(jsM.to_json())
  features_existing = get_features()
  feature_list = list()

  for country, cluster in countries_array.items():
    if not cluster in clusters.keys():
      countries = [country]
      clusters[cluster] = {"countries": countries}
    else:
      clusters[cluster]["countries"].append(country)


  for i, cluster in enumerate(KC):
    features = []

    for j, feature_mean_value in enumerate(cluster):
      features.append([features_existing[j][1],feature_mean_value])
    clusters[i]["features"] = features
    

  #print json.dumps(clusters, sort_keys=True, indent=4, separators=(',', ': '))

  return clusters



def clusterKMeans(liste_pays,features,nb_c) :

#INPUT:
#path="/home/DataVisProject/ms_bgd_projects/"
#path="/home/frederic/Visualisation/"
#countries="BEL,FRA,DEU,USA"
#si countries=""  Alors on prend tous les pays
#features="5,6,7,8,9,10,39"
#nb_c=2
#Le nb de cluster nb_c doit etre <= nb de countries selectionnes !
#OUTPUT:
#j_mat, json de la matrice : pour chaque pays, son numéro de cluster (méthode ecart-type)
#j_mat_D, json de la matrice : pour chaque pays, son numéro de cluster (méthode décile)
#KCenters, nd array indiquant les valeurs de chaque cluster sur ses axes (méthode écart-type)
#KCenters_D, nd array indiquant les valeurs de chaque cluster sur ses axes (methode décile)
#features: liste des features
#        dir=path
#        nomFic=dir+'factbookpro.csv'
        result = None

        data=pd.read_csv(current_path+"/static/factbookpro.csv",sep=';',header=0,index_col=0)
        colonnes=pd.Series(data.columns)
        nb_pays = 260
        if not len(liste_pays) == 0 :
          nb_pays=len(liste_pays)

        nb_clusters=int(nb_c)    
        
        
        if len(features) == 0:
          print("il faut selectionner au moins une colonne")

        else:
          liste=[]
          for i in features:
            liste.append(int(i))

  #        nb_features=len(lss)    

          if not len(liste_pays) == 0 :
            data=data.ix[liste_pays]

          param_col=pd.Series(colonnes.ix[liste])
          d_eco=data.loc[:,param_col]

          d_eco=d_eco.dropna()    

          mean=np.mean(d_eco)
          d_eco=d_eco-mean

          nb_pays, nb_features = d_eco.shape  
          if (nb_clusters>nb_pays):
                 print("le nb de clusters doit etre inf ou egal au nb de pays")
                 print("nb clusters ",nb_clusters, " nb pays apres cleaning ",nb_pays)
          else:

            estimator=KMeans(init='k-means++', n_clusters=nb_clusters, n_init=10)

            for i in liste :
    #   print(i) 
                   col=param_col[i]
    #   print(col)
    #reduction des colonnes :   
    #               norm=math.sqrt(np.dot(d_eco[col],d_eco[col]))
    #   d_eco[col]=d_eco[col]/norm
    #division par l'ecart-type :     
                   ec=np.std(d_eco[col])
                   d_eco[col]=d_eco[col]/ec
    #
            d_eco.to_csv(current_path+"/static/d_eco.csv", sep=";")
            
            estimator.fit(d_eco)  
            labels=estimator.labels_
            d_eco['cluster']=labels

    #DEB        print("taille des clusters KMeans sur colonnes centrees",d_eco.groupby('cluster').size())

            j_mat=d_eco['cluster']
            KCenters =estimator.cluster_centers_
            #print KCenters
            #j_centroids=pd.DataFrame(KCenters).to_json(orient='index')
    #calcul des deciles :
            col_analyse=[]
            for i in liste :
    #           print(i) 
               col=param_col[i]
    #           print(col)
    #   
               try : 
                  deciles = pd.qcut(d_eco[col], 10, labels=[1,2,3,4,5,6,7,8,9,10],precision=3)
               except ValueError:
                  deciles = pd.cut(d_eco[col], 10, labels=[1,2,3,4,5,6,7,8,9,10],precision=3) 
               d_eco['D'+str(i)]=deciles
               col_analyse.append('D'+str(i))
            
    #KMeans sur les deciles:  
            d_eco_analyse=d_eco.loc[:,col_analyse]
            estimator.fit(d_eco_analyse)  
            labels=estimator.labels_
            d_eco['cluster_d']=labels

    #DEB        print("taille des clusters KMeans sur colonnes deciles",d_eco.groupby('cluster_d').size())
            
            j_mat_D=d_eco['cluster_d']
            KCenters_D= estimator.cluster_centers_
            #print KCenters_D
            #j_centroids_d=pd.DataFrame().to_json(orient='index')

    #DEB        print features
            #return j_mat,j_mat_D,j_centroids,j_centroids_d,
            #return j_mat,j_mat_D, KCenters ,KCenters_D, features
            return beautiful_json_cluster(j_mat,KCenters,features)
 
 
def clusterKMeans_Test():
    #jsM,jsM_D,jsC,jsC_D=clusterKMeans("/home/frederic/Visualisation/","","13,14,24,34",8)
    #jsM,jsM_D,jsC,jsC_D=clusterKMeans("/home/xubuntu/","","13,14,24,34",8)
    #jsM,jsM_D,KC,KC_D,FT =clusterKMeans("/home/xubuntu/","","13,14,24,34",8)
    clusterKMeans(["AFG","ALB","DZA","ASM","AND","AGO","AIA","ATA","ATG","ARG","ARM","ABW","AUS","AUT","AZE","BHS","BHR","ISL","BGD","BRB","BLR","BEL","BLZ","BEN","BMU","BTN","BOL","BIH","BWA","BVT","BRA","IOT","JPN","JEY","JON","JOR","KAZ","KEN","KIR","PRK","KOR","KWT","KGZ","LAO","LVA","LBN","LSO","LBR","LBY","LIE","LTU","LUX","MAC","MKD","MDG","MWI","MYS","MDV","MLI","MLT","MHL","MTQ","MRT","MUS","MYT","MEX","FSM","MDA","MCO","MNG","MSR","MAR","MOZ","NAM","FRA", "GER", "TUR", "TKM","TCA","TUV","UGA","UKR","ARE","GRB","USA","URY","UZB","VUT","VEN","VNM","VGB"],[13,14,24,34],8)
    #print jsM
    #print jsM_D
    #print KC
    #print KC_D
    #print FT   #features
    









