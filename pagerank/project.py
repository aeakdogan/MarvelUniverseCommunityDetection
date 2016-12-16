import codecs
import collections
import operator
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt

def create_matrix(filepath):
   # total 6486 different nodes so create 6486 x 6486 adjocency matrix
   adjocency_matrix = np.zeros(shape=(6486, 6486))
   with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        line = line.replace(" ", "")  #remove white space
        linesplit = line.split(',')
        if(linesplit[0] != "vertex1"):
            vertex1 = int(linesplit[0])
            vertex2 = int(linesplit[1])
            weight = int(linesplit[2])
            adjocency_matrix[vertex1-1][vertex2-1] = weight; # -1 becuase of node index difference
            adjocency_matrix[vertex2-1][vertex1-1] = weight;

    return adjocency_matrix

def simrank(G, r=0.8, max_iter=100, eps=1e-4):

    nodes = G.nodes()
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = np.zeros(len(nodes))
    sim = np.identity(len(nodes))

    for i in range(max_iter):
        if np.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = np.copy(sim)
        for u, v in itertools.product(nodes, nodes):
            if u is v:
                continue
            u_ns, v_ns = G.predecessors(u), G.predecessors(v)

            # evaluating the similarity of current iteration nodes pair
            if len(u_ns) == 0 or len(v_ns) == 0:
                # if a node has no predecessors then setting similarity to zero
                sim[nodes_i[u]][nodes_i[v]] = 0
            else:
                s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
                sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / (len(u_ns) * len(v_ns))


    return sim


def general_pagerank(graph):
    personalize = dict((n, 0) for n in graph)
    personalize[5305] = 1000;
    pagerank = nx.pagerank(graph, max_iter=300)
    nodes_indexes = pagerank.items()
    nodes_by_rank = sorted(
        nodes_indexes, key=operator.itemgetter(1), reverse=True)
    print(nodes_by_rank)

def topic_specific_pagerank(graph):
    personalize = dict((n, 0) for n in graph)
    personalize[1601] = 100; #spiderman: 5305, ironman:2663,  WOLVERINE:6305 DEADPOOL: 1397, DR. STRANGE: 1601
    pagerank = nx.pagerank(graph, max_iter=50, personalization=personalize)
    nodes_indexes = pagerank.items()
    nodes_by_rank = sorted(
        nodes_indexes, key=operator.itemgetter(1), reverse=True)
    print(nodes_by_rank)
    return nodes_by_rank

def pagerank_to_plot(pagerank, center):
    G = nx.Graph()

    for ind, val in enumerate(pagerank):
        if(ind < 5):
            G.add_edge(center, val[0], weight=val[1])

    pos=nx.spring_layout(G) # positions for all nodes
    # nodes
    nx.draw_networkx(G)
    plt.axis("off")
    plt.show()


adj = create_matrix("./weighted_edges.txt")
graph = nx.from_numpy_matrix(adj) # create graph from ada
#general_pagerank(graph)
pg = topic_specific_pagerank(graph)
pagerank_to_plot(pg, 1601)



