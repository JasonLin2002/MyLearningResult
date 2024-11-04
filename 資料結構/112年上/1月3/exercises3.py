def greedy_coloring(edges, num_nodes, colors):
    color_assignment = [-1] * num_nodes
    
    color_assignment[0] = 0
    
    available = [False] * num_nodes
    
    for u in range(1, num_nodes):
        for v in edges[u]:
            if color_assignment[v] != -1:
                available[color_assignment[v]] = True
                
        cr = 0
        while cr < num_nodes:
            if not available[cr]:
                break
            cr += 1
        
        color_assignment[u] = cr
        
        for v in edges[u]:
            if color_assignment[v] != -1:
                available[color_assignment[v]] = False
                
    return [colors[color] for color in color_assignment]

def convert_to_adj_list(edges, num_nodes):
    adj_list = {i: [] for i in range(num_nodes)}
    for (u, v) in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list

colors = ['BLUE', 'GREEN', 'RED', 'YELLOW', 'ORANGE', 'PINK', 'BLACK', 'BROWN', 'WHITE', 'PURPLE', 'VOILET']
edges = [(0, 1), (0, 4), (0, 5), (4, 5), (1, 4), (1, 3), (2, 3), (2, 4)]
num_nodes = 6

adj_list = convert_to_adj_list(edges, num_nodes)

coloring = greedy_coloring(adj_list, num_nodes, colors)
print("節點著色分配:", coloring)