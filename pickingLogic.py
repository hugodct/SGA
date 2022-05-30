import pandas as pd
import networkx as nx

def generate_nodes(data):
    nodes_df = pd.DataFrame(columns=['Id', 'Codigo', 'Habilitado', 'IdAlmacen', 'PosX', 'PosY', 'PosZ', 'IdContenedor'])

    for i in range(len(data)):  # creacion del dataframe de nodos
        ubi = data[i]
        nodes_df.loc[i] = [ubi["Id"], ubi["Codigo"], ubi["Habilitado"], ubi["IdAlmacenInteligente"],
                           ubi["PlanoCoordenadaX"], ubi["PlanoCoordenadaY"], ubi["PlanoCoordenadaZ"],
                           ubi["IdContenedor"]]

    #MANUAL TABLE PIVOT
    df2 = nodes_df.iloc[1::2]
    contenedoresB = df2[['IdContenedor']]
    contenedoresB.reset_index(drop=True, inplace=True)
    contenedoresB.rename(columns={"IdContenedor": "IdContenedorB"}, inplace=True)

    r = list(range(1, len(data), 2))

    nodes_df.drop(r, inplace=True)
    nodes_df.reset_index(drop=True, inplace=True)

    nodes_df = nodes_df.join(contenedoresB)
    nodes_df.drop(columns=['PosZ'], inplace=True)

    nodes_df['NodeName'] = nodes_df["PosX"].astype(str) + nodes_df["PosY"].astype(str) #Generate nodename for tsp

    return nodes_df

def generate_edges(nodes_df):
    edges_df = pd.DataFrame(columns=['Source', 'Target', 'Type', 'weight', 'color'])
    shape = [int(nodes_df['PosX'].max()),int(nodes_df['PosY'].max())]

    node_list = list(nodes_df["PosX"].astype(str) + nodes_df["PosY"].astype(str))

    k = int(0)  # Generar edges de columnas
    for i in range(1, shape[0] + 1):
        for j in range(1, shape[1]):
            nodo_anterior = str(i) + str(j)
            if nodo_anterior in node_list: #Comprobar si el nodo origen existe antes de añadir la arista
                nodo_actual = str(i) + str(j + 1)
                edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
            k += 1

    IPASILLOS = range(shape[1]+1)
    for j in range(1, shape[1] + 1):  # Generar edges de filas
        if j in IPASILLOS:
            for i in range(1, shape[0]):
                nodo_anterior = str(i) + str(j)
                if nodo_anterior in node_list: #Comprobar si el nodo origen existe antes de añadir la arista
                    nodo_actual = str(i + 1) + str(j)
                    edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
                k += 1

    return edges_df
