import networkx as nx
import json
import matplotlib.pyplot as plt

with open('graf.json', 'r') as json_file:
    json_data = json.load(json_file)

Gr = nx.node_link_graph(json_data)

Gr.remove_node('Wrocław Główny')
Gr.remove_node('Wrocław Grabiszyn')
Gr.remove_node('Wrocław Muchobór')

plt.figure(figsize=(10, 8))
pos = nx.kamada_kawai_layout(Gr)
nx.draw(Gr, pos, with_labels=True, font_weight='bold')
plt.show()


degree_hist = nx.degree_histogram(Gr)
plt.subplot(2, 2, 1)
plt.bar(range(len(degree_hist)), degree_hist)
plt.xlabel("Stopień węzła")
plt.ylabel("Liczność")
plt.title("Histogram stopni węzłów")

closeness = nx.closeness_centrality(Gr)
betweenness = nx.betweenness_centrality(Gr)
degree_values = nx.degree_centrality(Gr)

sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
sorted_degree = sorted(degree_values.items(), key=lambda x: x[1], reverse=True)

print("Sorted Closeness Centrality:")
print(sorted_closeness)
print("\nSorted Betweenness Centrality:")
print(sorted_betweenness)
print("\nSorted Degree Centrality:")
print(sorted_degree)

plt.subplot(2, 2, 2)
plt.scatter(list(closeness.values()), list(betweenness.values()))
plt.xlabel("Bliskość (Closeness)")
plt.ylabel("Pośrednictwo (Betweenness)")
plt.title("Scatter plot: Bliskość vs. Pośrednictwo")

plt.subplot(2, 2, 3)
plt.bar(range(len(sorted_closeness)), [x[1] for x in sorted_closeness])
plt.xlabel("Węzeł")
plt.ylabel("Bliskość (Closeness)")
plt.title("Sorted Closeness Centrality")

plt.subplot(2, 2, 4)
plt.bar(range(len(sorted_betweenness)), [x[1] for x in sorted_betweenness])
plt.xlabel("Węzeł")
plt.ylabel("Pośrednictwo (Betweenness)")
plt.title("Sorted Betweenness Centrality")

plt.tight_layout()
plt.show()


top_przystanki = [item[0] for item in sorted_betweenness[:10]]
top_posrednictwo = [item[1] for item in sorted_betweenness[:10]]

plt.subplot(2, 2, 1)
plt.bar(top_przystanki, top_posrednictwo, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Pośrednictwo')
plt.title('Top 10 przystanków pod względem pośrednictwa')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


top_przystanki = [item[0] for item in sorted_closeness[:10]]
top_bliskosc = [item[1] for item in sorted_closeness[:10]]

plt.subplot(2, 2, 2)
plt.bar(top_przystanki, top_bliskosc, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Bliskość')
plt.title('Top 10 przystanków pod względem Bliskości')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


top_przystanki = [item[0] for item in sorted_degree[:10]]
top_stopien = [item[1] for item in sorted_degree[:10]]

plt.subplot(2, 2, 3)
plt.bar(top_przystanki, top_stopien, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Stopień')
plt.title('Top 10 przystanków pod względem stopnia')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()