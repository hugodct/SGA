from flask import Flask,request
import algoritmos_sga as al
import networkx as nx

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

if __name__ == "__main__":
    app.run(debug=True)