import matplotlib.pyplot as plt
import networkx as nx
from queue import Queue

edges = [
    ('a', 'b'), ('a', 'c'), ('a', 'e'),
    ('b', 'c'),
    ('c', 'd'), ('c', 'e'), ('c', 'f'),
    ('d', 'f'), ('d', 'g'),
    ('e', 'f'),
    ('f', 'g'), ('f', 'h')
]

G = nx.Graph()
G.add_edges_from(edges)

plt.figure(figsize=(10, 5))
nx.draw(G, with_labels=True, font_weight='bold', node_size=700, font_size=18)
plt.title("Graph based on the provided image")
plt.show()

adj_matrix = nx.adjacency_matrix(G).todense()

def bfs(graph, start):
    visited = set()
    queue = Queue()
    bfs_order = []
    queue.put(start)
    visited.add(start)
    while not queue.empty():
        vertex = queue.get()
        bfs_order.append(vertex)
        for neighbour in sorted(list(graph.neighbors(vertex))):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.put(neighbour)
    return bfs_order

bfs_order = bfs(G, 'a')

print("Adjacency Matrix:")
print(adj_matrix)

print("\nBFS Order starting from node 'a':")
print(bfs_order)

bfs_edges = [(bfs_order[i], bfs_order[i + 1]) for i in range(len(bfs_order) - 1)]
bfs_tree = nx.Graph()
bfs_tree.add_edges_from(bfs_edges)

plt.figure(figsize=(10, 5))
nx.draw(bfs_tree, with_labels=True, font_weight='bold', node_size=700, font_size=18)
plt.title("BFS Tree starting from node 'a'")
plt.show()