import networkx as nx
import json
import matplotlib.pyplot as plt

with open('graf.json', 'r') as json_file:
    json_data = json.load(json_file)

Gr = nx.node_link_graph(json_data)

wroclaw_nodes = []
for node in Gr:
    if node.startswith('Wrocław'):
        wroclaw_nodes.append(node)

wroclaw_nodes.append('Jeżyny')

H = Gr.subgraph(wroclaw_nodes)

closeness = nx.closeness_centrality(Gr)
betweenness = nx.betweenness_centrality(Gr)
degree_values = nx.degree_centrality(Gr)

sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
sorted_degree = sorted(degree_values.items(), key=lambda x: x[1], reverse=True)


wroclaw_degree_ranking = [item for item in sorted_degree if item[0] in wroclaw_nodes]
wroclaw_betweenness_ranking = [item for item in sorted_betweenness if item[0] in wroclaw_nodes]
wroclaw_closeness_ranking = [item for item in sorted_closeness if item[0] in wroclaw_nodes]

# Wydrukuj rankingi
print("Wroclaw Degree Ranking:")
print(wroclaw_degree_ranking)

print("\nWroclaw Betweenness Centrality Ranking:")
print(wroclaw_betweenness_ranking)

print("\nWroclaw Closeness Centrality Ranking:")
print(wroclaw_closeness_ranking)

top_przystanki = [item[0] for item in wroclaw_betweenness_ranking[:5]]
top_posrednictwo = [item[1] for item in wroclaw_betweenness_ranking[:5]]

plt.subplot(2, 2, 1)
plt.bar(top_przystanki, top_posrednictwo, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Pośrednictwo')
plt.title('Top 10 przystanków pod względem pośrednictwa')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


top_przystanki = [item[0] for item in wroclaw_closeness_ranking[:5]]
top_bliskosc = [item[1] for item in wroclaw_closeness_ranking[:5]]

plt.subplot(2, 2, 2)
plt.bar(top_przystanki, top_bliskosc, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Bliskość')
plt.title('Top 10 przystanków pod względem Bliskości')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


top_przystanki = [item[0] for item in wroclaw_degree_ranking[:5]]
top_stopien = [item[1] for item in wroclaw_degree_ranking[:5]]

plt.subplot(2, 2, 3)
plt.bar(top_przystanki, top_stopien, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Stopień')
plt.title('Top 10 przystanków pod względem stopnia')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()

plt.figure(figsize=(10, 8))
pos = nx.kamada_kawai_layout(H)
nx.draw(H, pos, with_labels=True, font_weight='bold')
plt.show()
