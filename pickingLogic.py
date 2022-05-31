import pandas as pd
import networkx as nx

def generate_nodes(data):
    nodes_df = pd.DataFrame(columns=['Id', 'Codigo', 'Habilitado', 'IdAlmacen', 'PosX', 'PosY', 'PosZ',
                                     'IdContenedor', 'ContenidoCodigo1','ContenidoCodigo2','ContenidoCodigo3','ContenidoUds1','ContenidoUds2','ContenidoUds3'])

    for i in range(len(data)):  #creacion del dataframe de nodos
        ubi = data[i]
        nodes_df.loc[i] = [ubi["Id"], ubi["Codigo"], ubi["Habilitado"], ubi["IdAlmacenInteligente"],
                           ubi["PlanoCoordenadaX"], ubi["PlanoCoordenadaY"], ubi["PlanoCoordenadaZ"],
                           ubi["IdContenedor"], ubi["ContenidoCodigo1"], ubi["ContenidoCodigo2"], ubi["ContenidoCodigo3"],
                           ubi["ContenidoUds1"], ubi["ContenidoUds2"], ubi["ContenidoUds3"]]

    nodes_df['ContenidoA'] = nodes_df["ContenidoCodigo1"].astype(str) + "," + nodes_df["ContenidoCodigo2"].astype(str) + "," + nodes_df["ContenidoCodigo3"].astype(str)
    nodes_df['UnidadesA'] = nodes_df["ContenidoUds1"].astype(str) + "," + nodes_df["ContenidoUds2"].astype(str) + "," + nodes_df["ContenidoUds3"].astype(str)

    #MANUAL TABLE PIVOT
    df2 = nodes_df.iloc[1::2] #select odd rows
    height1_df = pd.concat([df2['IdContenedor'], df2['ContenidoA'], df2['UnidadesA']], axis=1, keys=['IdContenedorB', 'ContenidoB', 'UnidadesB'])

    height1_df.reset_index(drop=True, inplace=True)

    r = list(range(1, len(data), 2)) #[1,3,...,(2n-1)]

    nodes_df.drop(r, inplace=True)
    nodes_df.reset_index(drop=True, inplace=True)

    nodes_df = nodes_df.join(height1_df)
    nodes_df.drop(columns=['PosZ','ContenidoCodigo1','ContenidoCodigo2','ContenidoCodigo3','ContenidoUds1','ContenidoUds2','ContenidoUds3'], inplace=True)
    nodes_df.rename(columns={'IdContenedor': 'IdContenedorA'}, inplace=True)

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

def get_nodes_where_container(nodes_df, containers, first_node):
    indices = [first_node]  # Get nodes from list of containers

    for i in range(len(containers)):
        if str(containers[i]) in nodes_df['IdContenedorA'].values:
            indice = nodes_df.index[nodes_df['IdContenedorA'] == str(containers[i])].tolist()
        elif str(containers[i]) in nodes_df['IdContenedorB'].values:
            indice = nodes_df.index[nodes_df['IdContenedorB'] == str(containers[i])].tolist()

        indices.append(indice[0])

    nodos = []  # Idem
    for i in range(len(containers)+1):
        nodo = nodes_df.iloc[indices[i], -1]
        nodos.append(nodo)

    return nodos


def get_nodes_where_article(nodes_df, articles):
    node_dict = {}  #Gets list of articles, returns node and height of possible retrieval

    for i in range(len(articles)):
        node_list = []

        art = list(articles.keys())[i]
        cantidad_solicitada = articles[art]

        for j in range(nodes_df.shape[0]):
            cont_A_string = nodes_df.loc[nodes_df.index[j],'ContenidoA'].split(',')
            cont_B_string = nodes_df.loc[nodes_df.index[j],'ContenidoB'].split(',')

            uds_A_string = nodes_df.loc[nodes_df.index[j],'UnidadesA'].split(',')
            uds_B_string = nodes_df.loc[nodes_df.index[j], 'UnidadesB'].split(',')

            A_dict = dict(zip(cont_A_string, uds_A_string))
            B_dict = dict(zip(cont_B_string, uds_B_string))

            if art in cont_A_string and A_dict[art] >= cantidad_solicitada:
                node_list.append([nodes_df.loc[nodes_df.index[j],'NodeName'],'A'])

            elif art in cont_B_string and B_dict[art] >= cantidad_solicitada:
                node_list.append([nodes_df.loc[nodes_df.index[j],'NodeName'],'B'])

        node_dict[art] = node_list

    return node_dict

def meta_heuristic(pr):
    print(pr)
    n = 1
    for articulo in pr:
        positions = len(pr[articulo])
        n = n * positions

    if n > 20:
        return 0 #Too many combinations

    else:
        for i in range(n):
            pass

    pass