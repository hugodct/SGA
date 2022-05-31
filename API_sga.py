from flask import Flask,request
import pickingLogic as al
import networkx as nx
import pandas as pd
pd.set_option('display.max_columns', None)


app = Flask(__name__)

@app.route('/gen_warehouse', methods=['POST'])
def generate_warehouse():
    data = request.get_json()

    nodes_df = al.generate_nodes(data)
    edges_df = al.generate_edges(nodes_df)
    print(nodes_df)
    print(edges_df)

    nodes_df.to_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Nodes.pkl')
    edges_df.to_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Edges.pkl')

    return "Warehouse generated successfully"


@app.route('/container_picking', methods=['POST'])
def do_container_picking():
    edges_df = pd.read_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Edges.pkl')
    nodes_df = pd.read_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Nodes.pkl')
    container_list = request.get_json()
    print(edges_df)
    print(nodes_df)

    G = nx.from_pandas_edgelist(edges_df,
                                source='Source',
                                target='Target',
                                edge_attr=["weight", "color"])

    nodos = al.get_nodes_where_container(nodes_df, container_list, 0)

    tsp = nx.approximation.traveling_salesman_problem
    path = tsp(G, nodes=nodos, cycle=True)

    keys = list(range(1,len(path)))
    path_dict = dict(zip(keys, path))

    return path_dict


@app.route('/article_picking', methods=['POST'])
def do_article_picking():
    edges_df = pd.read_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Edges.pkl')
    nodes_df = pd.read_pickle(r'C:\Users\LENOVO\PycharmProjects\almacen\Nodes.pkl')
    article_dict = request.get_json()

    print(edges_df)
    print(nodes_df)
    print(article_dict)

    possible_retrievals = al.get_nodes_where_article(nodes_df, article_dict)
    al.meta_heuristic(possible_retrievals)


    return article_dict


if __name__ == "__main__":
    app.run(debug=True)