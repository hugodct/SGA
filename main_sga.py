import algoritmos_sga as al
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib


NROWS = 7
NCOLUMNS = 10
IPASILLOS = [1,4,7] #Filas en las que hay pasillo horizontal

edges_df = al.generate_warehouse_edges(NROWS,NCOLUMNS,IPASILLOS)
nodes_df = al.generate_warehouse_nodes(NROWS, NCOLUMNS)
print(nodes_df)

pos = nodes_df.drop(columns=['Ref'])
pos = pos.set_index('Node').T.to_dict('list')

G = nx.from_pandas_edgelist(edges_df,
                            source='Source',
                            target='Target',
                            edge_attr=["weight", "color"])

tsp = nx.approximation.traveling_salesman_problem
path = tsp(G, nodes=["11","46","83"])
print("Path",path, len(path))

for i in range(len(path)-1):
    G.add_edge(path[i],path[i+1],color='red')

edges = G.edges()
colors = [G[u][v]['color'] for u, v in edges]
widths = [G[u][v]['weight'] for u, v in edges]

widths = [x * 3 for x in widths]

nx.draw_networkx(G,pos=pos, node_size = 350, linewidths=5, edge_color=colors, width=widths, font_size=10, font_family='Lucida Sans')

indices = al.get_references_optimize(edges_df, nodes_df, [101,102,103])
print(indices, type(indices[0]))
