import codecs
import networkx as nx
import matplotlib.pyplot as plt
import time

edges = {}


def main():
    start_time = time.time()
    G = nx.cubical_graph()

    edges_list = []
    all_edges = []
    line_count = 0
    n = 0
    outputFile = open('../outputs/communities.txt', 'w+')
    #with codecs.open("../inputs/sampleInput.txt", 'r', encoding='utf-8', errors='ignore') as file:
    with codecs.open("../inputs/weighted_edges.txt", 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if line_count == 0:
                line_count += 1
                continue
            tmp = [int(num) for num in line.split(', ')]
            vertex1 = tmp[0]
            vertex2 = tmp[1]
            weight = tmp[2]

            n = max(n, vertex1, vertex2)

            if vertex1 not in edges:
                edges[vertex1] = [[vertex2, weight]]
            else:
                edges[vertex1].append([vertex2, weight])

            if vertex2 not in edges:
                edges[vertex2] = [[vertex1, weight]]
            else:
                edges[vertex2].append([vertex1, weight])

            G.add_edge(vertex1, vertex2, weight=weight)
            G.add_edge(vertex2, vertex1, weight=weight)

            edges_list.append([vertex1, vertex2, weight])
            all_edges.append((vertex1, vertex2))
            all_edges.append((vertex2, vertex1))
            line_count += 1
    time2 = time.time()
    print("reading edges completed in --- %s seconds ---" % (time2 - start_time))

    for i in range(1, n + 1):
        if i not in edges:
            G.add_node(i)
            edges[i] = []

    communities = []

    #with codecs.open("../inputs/sample_communities.txt", 'r', encoding='utf-8', errors='ignore') as file:
    with codecs.open("../inputs/marvel_communities.txt", 'r', encoding='utf-8', errors='ignore') as file:

        for line in file:
            line = line.rstrip('\n').replace('[', '').replace(']', '')
            tmp = line.split(' ', 1)[1]

            communities.append([int(node) for node in tmp.split(', ')])
    # print(communities)
    time3 = time.time()
    print("reading communitites completed in --- %s seconds ---" % (time3 - time2))
    time1 = time.time()
    pos = nx.spring_layout(G)
    #pos = nx.circular_layout(G)
    #pos = nx.nx_pydot.graphviz_layout(G)
    time2 = time.time()
    print("graph is arranged in --- %s seconds ---" % (time2 - time1))
    # print(all_edges)
    # print(G.nodes())
    # print(G.edges())
    # print(pos)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=range(1, n + 1),
                           node_color='b',
                           node_size=100,
                           alpha=0.8)

    colors = ['r', 'b', 'y', 'w', 'g', 'c']
    labels = {}
    for i in range(n + 1):
        labels[i] = i
        # labels[i] = chr(ord('a') + i - 1)

    time1 = time.time()
    communities.sort(key=lambda s: len(s), reverse=True)
    time2 = time.time()
    print("communities sorted in --- %s seconds ---" % (time2 - time1))
    for (i, community) in enumerate(communities):
        #print(i, community)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=community,
                               node_color=colors[i % 6],
                               node_size=10,
                               alpha=0.8)

    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=all_edges,
                           width=2, alpha=0.5, edge_color='r')
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    plt.show()


main()
