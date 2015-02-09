#from django.db import models

# Create your models here.
import pandas as pd
#import csv
import numpy as np
#import matplotlib.pyplot as plt
import sys 
#import math
from sklearn.cluster import KMeans

def clusterKMeans(path,countries,features,nb_c) :
#path="/home/DataVisProject/ms_bgd_projects/"
#path="/home/frederic/Visualisation/"
#countries="BEL,FRA,DEU,USA"
#si countries=""  Alors on prend tous les pays
#features="5,6,7,8,9,10,39"
#nb_c=2
#Le nb de cluster nb_c doit etre <= nb de countries selectionnes !
        dir=path
        nomFic=dir+'factbookpro.csv'
              
        data=pd.read_csv(nomFic,sep=';',header=0,index_col=0)
        colonnes=pd.Series(data.columns)
        ls_pays=countries
        liste_pays=ls_pays.split(',')
        nb_pays = 260
        if not ls_pays=="" :
               nb_pays=len(liste_pays)

        nb_clusters=int(nb_c)    
        
        ls=features
        if (ls==""):
                print("il faut selectionner au moins une colonne")
                sys.exit(1)

        lss=ls.split(',')
        liste=[]
        for i in lss:
                 liste.append(int(i))

#        nb_features=len(lss)    

        if not ls_pays=="" :
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
               sys.exit(0)

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
        estimator.fit(d_eco)  
        labels=estimator.labels_
        d_eco['cluster']=labels

        print("taille des clusters KMeans sur colonnes centrees",d_eco.groupby('cluster').size())

        j_mat=d_eco['cluster'].to_json()
        j_centroids=pd.DataFrame(estimator.cluster_centers_).to_json(orient='index')

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

        print("taille des clusters KMeans sur colonnes deciles",d_eco.groupby('cluster_d').size())

        j_centroids_d=pd.DataFrame(estimator.cluster_centers_).to_json(orient='index')

        j_mat_D=d_eco['cluster_d'].to_json()
        
        return j_mat,j_mat_D,j_centroids,j_centroids_d
         
            
        
jsM,jsM_D,jsC,jsC_D=clusterKMeans("/home/frederic/Visualisation/","","13,14,24,34",8)




