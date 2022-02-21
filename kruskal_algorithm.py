import itertools

def kruskal(edges):
    edges = list(edges)
    edges.sort(key=lambda x: x[-1])
    edges = [(edge[0], edge[1]) for edge in edges]
    node_sets = [{i} for i in set(itertools.chain(*edges))]
    kruskal_edges = []
    while len(node_sets) != 1:
        for edge in edges:
            edge_sets = []
            for node_set in node_sets:
                if ({edge[0]}.issubset(node_set) and not {edge[1]}.issubset(node_set)) or ({edge[1]}.issubset(node_set) and not {edge[0]}.issubset(node_set)):
                    edge_sets.append(node_set)

                elif {edge[0]}.issubset(node_set) and {edge[1]}.issubset(node_set):
                    break
            if len(edge_sets) == 2:
                node_sets.append(edge_sets[0].union(edge_sets[1]))
                del node_sets[node_sets.index(edge_sets[0])]
                del node_sets[node_sets.index(edge_sets[1])]
                kruskal_edges.append((edge))
                del edges[edges.index(edge)]
                break

    return kruskal_edges

