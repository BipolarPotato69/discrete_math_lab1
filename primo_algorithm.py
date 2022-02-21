import itertools
import random

def primo(edges):

    edges = list(edges)
    edges.sort(key=lambda x: x[-1])
    edges = [(edge[0], edge[1]) for edge in edges]
    picked_nodes = {random.choice(list(itertools.chain(*edges)))}
    primo_edges = []
    node_set = len(set(itertools.chain(*edges)))
    while len(picked_nodes) != node_set:
        for edge in edges:
            if (edge[0] in picked_nodes and not edge[1] in picked_nodes):
                primo_edges.append(edge)
                picked_nodes.add(edge[1])
                del edges[edges.index(edge)]
                break
            elif (edge[1] in picked_nodes and not edge[0] in picked_nodes):
                primo_edges.append(edge)
                picked_nodes.add(edge[0])
                del edges[edges.index(edge)]
                break

    return primo_edges
