from flask import Flask,request
import algoritmos_sga as al
import networkx as nx
import pandas as pd
pd.set_option('display.max_columns', None)


app = Flask(__name__)

@app.route('/picking',methods=['POST'])
def do_picking():
    dict_refs = request.args
    res = dict_refs['SKU'].split(",")
    refs = list(map(int, res))

    NROWS = 7
    NCOLUMNS = 10
    IPASILLOS = [1, 4, 7]  # Filas en las que hay pasillo horizontal

    edges_df = al.generate_warehouse_edges(NROWS, NCOLUMNS, IPASILLOS)
    nodes_df = al.generate_warehouse_nodes(NROWS, NCOLUMNS)

    G = nx.from_pandas_edgelist(edges_df,
                                source='Source',
                                target='Target',
                                edge_attr=["weight", "color"])
    nx.set_node_attributes(G, 'blue', name='color')

    path, nodos = al.get_references_tsp(edges_df, nodes_df, refs)

    path_dict = {i: path[i] for i in range(0, len(path))}

    return path_dict


@app.route('/gen_warehouse', methods=['POST'])
def generate_warehouse():
    data = request.get_json()
    nodes_df = pd.DataFrame(columns=['Id', 'Codigo', 'Habilitado', 'IdAlmacen', 'PosX', 'PosY', 'PosZ', 'IdContenedor', 'color'])

    for i in range(len(data)): #creacion del dataframe de nodos
        ubi = data[i]
        nodes_df.loc[i] = [ubi["Id"], ubi["Codigo"], ubi["Habilitado"], ubi["IdAlmacenInteligente"], ubi["PlanoCoordenadaX"], ubi["PlanoCoordenadaY"], ubi["PlanoCoordenadaZ"], ubi["IdContenedor"], 'blue']
    print(nodes_df)

    for i in range(0,len(data),2): #compresion para evitar coordenada Z
        nodes_df.iloc[i,7] = nodes_df.iloc[i,7] + "," + nodes_df.iloc[i+1,7]
    for i in range(0,len(data),2):
        nodes_df = nodes_df.drop([i + 1])
    nodes_df.drop(columns=['PosZ'], inplace=True)
    print(nodes_df)


    edges_df = pd.DataFrame(columns=['Source', 'Target', 'Type', 'weight', 'color'])
    shape = [int(nodes_df['PosX'].max()),int(nodes_df['PosY'].max())]

    k = int(0)  # Generar edges de columnas
    for i in range(1, shape[0] + 1):
        for j in range(1, shape[1]):
            nodo_actual = str(i) + str(j + 1)
            nodo_anterior = str(i) + str(j)
            edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
            k += 1

    IPASILLOS = range(shape[1]+1)
    for j in range(1, shape[1] + 1):  # Generar edges de filas
        if j in IPASILLOS:
            for i in range(1, shape[0]):
                nodo_actual = str(i + 1) + str(j)
                nodo_anterior = str(i) + str(j)
                edges_df.loc[k] = [nodo_anterior, nodo_actual, "Undirected", 1, "black"]
                k += 1

    print(edges_df)


    return {"yes":"test"}




if __name__ == "__main__":
    app.run(debug=True)