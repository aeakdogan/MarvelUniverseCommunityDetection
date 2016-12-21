import codecs
import networkx as nx
import matplotlib.pyplot as plt
import time

edges = {}
heroesNames = {5306: 'SPIDER-MAN', 859: 'CAPTAIN AMERICA', 2664: 'IRON MAN', 5716: 'THING', 5736: 'THOR',
               2557: 'HUMAN TORCH', 3805: 'MR. FANTASTIC',
               2548: 'HULK', 6306: 'WOLVERINE', 2650: 'INVISIBLE WOMAN', 403: 'BEAST', 4898: 'SCARLET WITCH',
               6066: 'VISION'}

def main():
    start_time = time.time()
    G = nx.cubical_graph()

    edges_list = []
    all_edges = []
    line_count = 0
    n = 0
    populars = []
    # with codecs.open("../inputs/sampleInput.txt", 'r', encoding='utf-8', errors='ignore') as file:
    with codecs.open("../pagerank/idfile.txt", 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # print(int(line))
            populars.append(int(line))
    #outputFile = open('../outputs/communities.txt', 'w+')
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
            if weight > 5:
                if vertex1 not in edges:
                    edges[vertex1] = [[vertex2, weight]]
                else:
                    edges[vertex1].append([vertex2, weight])

                if vertex2 not in edges:
                    edges[vertex2] = [[vertex1, weight]]
                else:
                    edges[vertex2].append([vertex1, weight])

                G.add_edge(vertex1, vertex2, weight=weight)
                # G.add_edge(vertex2, vertex1, weight=weight)

                edges_list.append([vertex1, vertex2, weight])
            # if vertex1 in populars[:500] and vertex2 in populars[:500] and weight > 10:
            #    all_edges.append((vertex1, vertex2))
            # all_edges.append((vertex2, vertex1))
            line_count += 1
    time2 = time.time()
    print("reading edges completed in --- %s seconds ---" % (time2 - start_time))

    for i in range(1, n + 1):
        if i not in edges:
            G.add_node(i)
            edges[i] = []

    communities = []

    # with codecs.open("../outputs/communities.txt", 'r', encoding='utf-8', errors='ignore') as file:
    # with codecs.open("../inputs/sample_communities.txt", 'r', encoding='utf-8', errors='ignore') as file:
    with codecs.open("../inputs/marvel_communities.txt", 'r', encoding='utf-8', errors='ignore') as file:

        for line in file:
            line = line.rstrip('\n').replace('[', '').replace(']', '')
            tmp = line.split(' ', 1)[1]

            communities.append([int(node) for node in tmp.split(', ')])
    time3 = time.time()
    print("reading communitites completed in --- %s seconds ---" % (time3 - time2))
    time1 = time.time()
    pos = nx.spring_layout(G)
    time2 = time.time()
    print("graph is arranged in --- %s seconds ---" % (time2 - time1))



    # nx.draw_networkx_nodes(G, pos,
    #                        #nodelist=range(1, n + 1),
    #                        nodelist=populars[:100],
    #                        node_color='b',
    #                        node_size=10,
    #                        alpha=0.8)

    colors = ['r', 'b', 'y', 'w', 'g', 'c']
    labels = {}
    for i in range(n + 1):
        if i in populars[:12]:
            labels[i] = heroesNames[i]

    time1 = time.time()
    filtered_communities = communities[:5]
    filtered_communities.sort(key=lambda s: len(s), reverse=True)
    time2 = time.time()
    print("communities sorted in --- %s seconds ---" % (time2 - time1))
    for (i, community) in enumerate(filtered_communities):
        # print(i, community)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=[x for x in community if x in populars[100:2000]],
                               node_color=colors[i % 6],
                               node_size=10,
                               alpha=1)

        nx.draw_networkx_nodes(G, pos,
                               nodelist=[x for x in community if x in populars[5:100]],
                               node_color=colors[i % 6],
                               node_size=30,
                               alpha=1)

        nx.draw_networkx_nodes(G, pos,
                               nodelist=[x for x in community if x in populars[:10]],
                               node_color=colors[i % 6],
                               node_size=150,
                               alpha=1)
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    # nx.draw_networkx_edges(G, pos,
    #                         edgelist=all_edges,
    #                         width=1, alpha=0.5, edge_color='r')
    # nx.draw_networkx_labels(G, pos, [label for label in labels if label in populars[:100]], font_size=5)
    nx.draw_networkx_labels(G, pos, labels, font_size=9)
    plt.show()

main()
