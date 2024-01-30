import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network

G = nx.Graph()
siec = Network(directed=False, width='100%', bgcolor='#222222', font_color='white')

df = pd.read_csv('ufc_results_last_50.csv')

all_fighters = set(df['Fighter1']).union(set(df['Fighter2']))
for fighter in all_fighters:
    siec.add_node(fighter)

for index, row in df.iterrows():
    G.add_edge(row['Fighter1'], row['Fighter2'])
    siec.add_edge(row['Fighter1'], row['Fighter2'])

degree_hist = nx.degree_histogram(G)
plt.bar(range(len(degree_hist)), degree_hist)
plt.xlabel("Stopień węzła")
plt.ylabel("Liczność")
plt.title("Histogram stopni węzłów")
plt.show()

closeness = nx.closeness_centrality(G)
betweenness = nx.betweenness_centrality(G)
degree_values = nx.degree_centrality(G)

sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
sorted_degree = sorted(degree_values.items(), key=lambda x: x[1], reverse=True)

print(sorted_closeness)
print(sorted_betweenness)
print(sorted_degree)

siec.show_buttons()
siec.show('graf.html', notebook=False)
