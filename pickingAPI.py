from flask import Flask,request
import pickingLogic as al
import networkx as nx
import pandas as pd
pd.set_option('display.max_columns', None)


app = Flask(__name__)

@app.route('/gen_warehouse', methods=['POST'])
def generate_warehouse():
    data = request.get_json()
    print(data)

    nodes_df = al.generate_nodes(data)
    print(nodes_df)

    edges_df = al.generate_edges(nodes_df)
    print(edges_df)

    nodes_df.to_pickle(r'C:\Users\doeetlab\PycharmProjects\pythonAPI\pickingAPI\Nodes.pkl')
    edges_df.to_pickle(r'C:\Users\doeetlab\PycharmProjects\pythonAPI\pickingAPI\Edges.pkl')

    return "Warehouse generated correctly"


@app.route('/container_picking', methods=['POST'])
def do_picking():
    edges_df = pd.read_pickle(r'C:\Users\doeetlab\PycharmProjects\pythonAPI\pickingAPI\Edges.pkl')
    nodes_df = pd.read_pickle(r'C:\Users\doeetlab\PycharmProjects\pythonAPI\pickingAPI\Nodes.pkl')
    data = request.get_json()
    print(edges_df)
    print(nodes_df)

    G = nx.from_pandas_edgelist(edges_df,
                                source='Source',
                                target='Target',
                                edge_attr=["weight", "color"])

    indices = [0]  # Get nodes from list of refs
    for i in range(len(data)):
        indice = nodes_df.index[nodes_df['IdContenedorB'] == str(data[i])].tolist()
        indices.append(indice[0])

    nodos = []  # Idem
    for i in range(len(data)+1):
        nodo = nodes_df.iloc[indices[i], -1]
        nodos.append(nodo)

    tsp = nx.approximation.traveling_salesman_problem
    path = tsp(G, nodes=nodos, cycle=True)

    keys = list(range(1,len(path)))
    path_dict = dict(zip(keys, path))

    return path_dict


if __name__ == "__main__":
    app.run(debug=True)