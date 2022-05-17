import pandas as pd
import random
import networkx as nx
import matplotlib.pyplot as plt


NROWS = 5
NCOLUMNS = 4
IPASILLOS = [1,3,5] #Filas en las que hay pasillo horizontal

def generate_warehouse_edges(NROWS, NCOLUMNS, IPASILLOS):
    #GENERAR EL ALMACEN - EDGES
    edges_df = pd.DataFrame(columns = ['Source','Target','Type', 'weight', 'color'])

    k = int(0) #Generar edges de columnas
    for i in range(1, NCOLUMNS + 1):
        for j in range(1, NROWS):
            nodo_actual = str(i) + str(j+1)
            nodo_anterior = str(i) + str(j)
            edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
            k+=1

    for j in range(1, NROWS+1):
        if j in IPASILLOS:
            for i in range(1, NCOLUMNS):
                nodo_actual = str(i+1) + str(j)
                nodo_anterior = str(i) + str(j)
                edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
                k += 1

    return edges_df


def generate_warehouse_nodes(NROWS, NCOLUMNS):
    #GENERAR EL ALMACEN - NODES
    n = NROWS * NCOLUMNS
    nodes_df = pd.DataFrame(columns=['Node', 'PosX', 'PosY', 'Ref'])

    k = 0
    for i in range(1, NROWS+1):
        for j in range(1, NCOLUMNS+1):
            node = str(j) + str(i)
            nodes_df.loc[k] = [node, j, i, k+101]
            k += 1

    return nodes_df

def get_references_optimize(edges_df, nodes_df, refs):
    #CALCULATE OPTIMUM PICKING FOR LIST OF REFS
    G = nx.from_pandas_edgelist(edges_df,
                                source='Source',
                                target='Target',
                                edge_attr=["weight", "color"])

    indices = []
    for i in range(len(refs)):
        indice = nodes_df.index[nodes_df['Ref'] == refs[i]]
        indices.append(indice[0])

    tsp = nx.approximation.traveling_salesman_problem
    path = tsp(G, nodes=["11", "46", "83"])
    return indices
