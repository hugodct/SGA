import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


edges_data = np.array([["11","12","Undirected",1],
                       ["11","21","Undirected",1],
                       ["22","21","Undirected",1],
                       ["12","13","Undirected",1],
                       ["13","23","Undirected",1],
                       ["23","33","Undirected",1],
                       ["21","31","Undirected",1],
                       ["23","22","Undirected",1],
                       ["32","33","Undirected",1],
                       ["32","31","Undirected",1],
                       ["31","41","Undirected",1],
                       ["41","42","Undirected",1],
                       ["42","43","Undirected",1],
                       ["43","33","Undirected",1],
                       ["43","44","Undirected",1],
                       ["44","45","Undirected",1],
                       ["45","35","Undirected",1],
                       ["35","25","Undirected",1],
                       ["25","15","Undirected",1],
                       ["15","14","Undirected",1],
                       ["14","13","Undirected",1],
                       ["25","24","Undirected",1],
                       ["24","23","Undirected",1],
                       ["35","34","Undirected",1],
                       ["34","33","Undirected",1]])

nodes_data = np.array([["11", 1, 1, 200],
                       ["12", 1, 2, 201],
                       ["21", 2, 1, 202],
                       ["22", 2, 2, 203],
                       ["13", 1, 3, 204],
                       ["23", 2, 3, 205],
                       ["33", 3, 3, 206],
                       ["32", 3, 2, 207],
                       ["31", 3, 1, 208],
                       ["41", 4, 1, 209],
                       ["42", 4, 2, 210],
                       ["43", 4, 3, 211],
                       ["44", 4, 4, 212],
                       ["45", 4, 5, 213],
                       ["35", 3, 5, 214],
                       ["25", 2, 5, 215],
                       ["15", 1, 5, 216],
                       ["44", 4, 4, 217],
                       ["34", 3, 4, 218],
                       ["24", 2, 4, 219],
                       ["14", 1, 4, 220]])

pos = {}
for i in range(nodes_data.shape[0]):
    node = nodes_data[i,0]
    pos[node] = [int(nodes_data[i,1]),int(nodes_data[i,2])]

edges_df = pd.DataFrame(edges_data, columns = ['Source', 'Target','Type','weight'])
edges_df['color'] = 'black'
nodes_df = pd.DataFrame(nodes_data, columns = ['Node','PosX','PosY','Ref'])

edges_df = edges_df.astype({"weight": int})
nodes_df = nodes_df.astype({"PosX": int, "PosY" : int, "Ref" : int})

G = nx.from_pandas_edgelist(edges_df,
                            source='Source',
                            target='Target',
                            edge_attr=["weight", "color"])
print(G)
widths = edges_data[:,3].astype(int)

tsp = nx.approximation.traveling_salesman_problem
path = tsp(G, nodes=["11","33","35"])
print("Path",path, len(path))

for i in range(len(path)-1):
    G.add_edge(path[i],path[i+1],color='red')

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]

nx.draw_networkx(G,pos=pos,edge_color=colors, width=widths)
plt.show()