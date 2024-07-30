import matplotlib.pyplot as plt
import algoritmos_sga as al
import networkx as nx

NROWS = 7
NCOLUMNS = 10
IPASILLOS = [1,4,7] #Filas en las que hay pasillo horizontal

edges_df = al.generate_warehouse_edges(NROWS,NCOLUMNS,IPASILLOS)
nodes_df = al.generate_warehouse_nodes(NROWS, NCOLUMNS)
print(nodes_df)

pos = nodes_df.drop(columns=['Ref', 'color'])
pos = pos.set_index('Node').T.to_dict('list')

G = nx.from_pandas_edgelist(edges_df,
                            source='Source',
                            target='Target',
                            edge_attr=["weight", "color"])
nx.set_node_attributes(G, 'white', name='color')
nx.set_edge_attributes(G, 'white', name='color')

path, nodos = al.get_references_tsp(edges_df, nodes_df, [101,103,119,155,160])
print('Nodos', nodos, 'Coste', len(path), 'Path', path)

for i in range(len(path)-1): #Cambiar color del path
    G.add_edge(path[i],path[i+1],color='red')

for i in range(len(nodos)): #Cambiar color de los nodos
    G.add_node(nodos[i], color='red')

edges = G.edges() #Get attributes of edges
edge_colors = [G[u][v]['color'] for u, v in edges]
edge_widths = [G[u][v]['weight'] for u, v in edges]

edge_widths = [x * 3 for x in edge_widths]

knodes = G.nodes() #Get attributes of nodes
knode_colors = [knodes[u]['color'] for u in knodes]

plt.rcParams['axes.facecolor'] = '#202020'
plt.figure()
nx.draw_networkx(G, pos=pos, node_size = 350, node_color = knode_colors, linewidths=5, edge_color=edge_colors, width=edge_widths, font_size=10, font_family='Lucida Sans')
plt.show()

