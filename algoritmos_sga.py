import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


NROWS = 5
NCOLUMNS = 4
IPASILLOS = [1,3,5] #Filas en las que hay pasillo horizontal

#GENERAR EL ALMACEN
edges_df = pd.DataFrame(columns = ['Source','Target','Type', 'weight', 'color'])

k = int(0) #Generar edges de columnas
for i in range(1, NCOLUMNS + 1):
    for j in range(1, NROWS):
        nodo_actual = str(i) + str(j+1)
        nodo_anterior = str(i) + str(j)
        edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
        k+=1

for i in range(len(IPASILLOS)):
    for j in range(1, NCOLUMNS):
        pass

