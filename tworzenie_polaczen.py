from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import json


def read_and_clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    trasy = []
    cleaned_content = []
    i = 0
    for line in content[:-1]:
        line = line.strip()
        cleaned_content.append(line.split(','))
        trasy.append([])
        for przystanek in cleaned_content[i]:
            if przystanek.strip() not in ['Mapa linii', 'Mapka linii', 'Obiekty inżynierskie', 'Na trasie',
                'Budowle na trasie', 'Obiekty inżynierskie', 'Mosty i wiadukty', 'Tunele i inne obiekty',
                'Widoki z trasy', 'Budowle inyżierskie', 'Zdjęcia z trasy', 'Wiadukty', 'Inne obiekty', 'Tunele',
                'Budowle inżynierskie', 'Tunel', '(Harrachov)']:
                trasy[i].append(przystanek.strip())
        i += 1
    return trasy


def create_graph(trasy):
    G = Network(height="500px", width="100%", directed=False)
    Gr = nx.Graph()

    for line in trasy:
        if line[0] == 'Jelenia Góra' and line[-1] == 'Zebrzydowa':
            line[11] = 'Radłówka'
        for i in range(len(line)-1):
            G.add_node(line[i])
            G.add_node(line[i+1])
            G.add_edge(line[i], line[i+1])
            Gr.add_edge(line[i], line[i+1])

    return G, Gr

file_path = 'trasy.txt'
cleaned_content = read_and_clean_file(file_path)

cleaned_content[29] = ['Kłodzko Główne','Kłodzko Miasto','Kłodzko Nowe','Kłodzko Książek','Kłodzko Zagórze',
                       'Stary Wielisław', 'Polanica Zdrój', 'Szczytna', 'Duszniki Zdrój', 'Kulin Kłodzki',
                       'Lewin Kłodzki', 'Kudowa Zdrój', 'Kudowa Słone']

G, Gr = create_graph(cleaned_content)

print(Gr.number_of_nodes())

json_data = nx.node_link_data(Gr)
with open('graf.json', 'w') as json_file:
    json.dump(json_data, json_file)


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


plt.figure(figsize=(10, 8))
pos = nx.kamada_kawai_layout(Gr)
nx.draw(Gr, pos, with_labels=True, font_weight='bold')
plt.show()

print(nx.is_connected(Gr))
# G.show_buttons(filter_=['physics'])
G.show("graph.html", notebook=False)

