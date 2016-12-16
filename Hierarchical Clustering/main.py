import codecs
import numpy as np
import sys
import operator
from collections import OrderedDict

#  Hierarchical Clustering find local communities better, since it uses jaccard similarity,


class Community:
    def __init__(self, node_id, comm_id, is_centroid):
        self.id = node_id
        self.comm_id = comm_id
        self.is_centroid = is_centroid

    def __repr__(self):
        return '\nId: %s, Community ID: %s, Is Centroid: %s\n' % (self.id, self.comm_id, self.is_centroid)


def generate_adjacency_matrix(inputpath):
    # char_count = 6486
    # book_count = 12942
    char_book_dict = {}
    with codecs.open(inputpath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            linesplit = line.split()
            x = int(linesplit[0])
            y = [int(num) for num in linesplit[1:]]
            for cbook in y:
                if cbook not in char_book_dict:
                    char_book_dict[x] = y
                else:
                    char_book_dict[x] = char_book_dict[x].extend(y)

    return char_book_dict


def jaccard_distance(char1, char2):
    intersection = np.sum(char1 == char2)
    union = len(char1) + len(char2) - intersection

    jaccard_sim = float(intersection) / float(union)
    jaccard_dist = 1 - jaccard_sim

    return jaccard_dist


def generate_distance_dict(adj_matrix):
    # Define distance matrix
    distance_dict = {}

    # Jaccard Distance
    for char1 in adj_matrix.items():
        for char2 in adj_matrix.items():
            jaccard_dist = jaccard_distance(char1[1], char2[1])
            key_pair = (min(char1[0], char2[0]), max(char1[0], char2[0]))
            if char1[0] != char2[0] and key_pair not in distance_dict:
                distance_dict[key_pair] = jaccard_dist
        print('Preparing distance_matrix .. ')
    return distance_dict


def sum_sq(community, node, adj_matrix):
    sum = 0
    for n in community:
        if n.id != node.id:
            sum += np.square(jaccard_distance(adj_matrix[n.id], adj_matrix[node.id]))
    return sum


def assign_centroid(communities, community_nodes, adj_matrix):  # Community nodes is a list of node ids
    min_sq_dist = sys.maxsize
    index = 0
    for idx, node in enumerate(community_nodes):
        sq_dist = sum_sq(community_nodes, node, adj_matrix)
        index = idx if sq_dist < min_sq_dist else index
    communities[community_nodes[index].id].is_centroid = True


def find_min(distance_dict, communities):
    min_dist = sys.maxsize
    for item in distance_dict.items():
        key = item[0]
        value = item[1]
        if communities[key[0]].is_centroid and communities[key[1]].is_centroid and min_dist > value:
            min_dist = value
            min_dist_node1, min_dist_node2 = communities[key[0]], communities[key[1]]
            return min_dist_node1, min_dist_node2, min_dist
    return None


def community_members(communities, centroid1, centroid2):
    # Find all members and return
    # Set all members comm_id to new_id
    # Turn is_centroid attribute of centroid to False
    new_id = min(centroid1.comm_id, centroid2.comm_id)
    comm1 = []
    comm2 = []
    for i in range(1, len(communities)):
        if communities[i] == centroid1 or communities[i] == centroid2:
            communities[i].is_centroid = False
        if communities[i].comm_id == centroid1.comm_id:
            communities[i].comm_id = new_id  # Set new community id
            comm1.append(communities[i])
        elif communities[i].comm_id == centroid2.comm_id:
            communities[i].comm_id = new_id  # Set new community id
            comm2.append(communities[i])
    return comm1, comm2


def hierarchical_clustering(communities, dist_dict, adj_matrix):
    min_distance = 0
    while min_distance < 1:
        node1, node2, min_distance = find_min(dist_dict, communities)
        community1, community2 = community_members(communities, node1, node2)
        combined_community = community1 + community2
        assign_centroid(communities, combined_community, adj_matrix)


def main():
    print('Generating Distance Matrix, Please Wait(~ 8 min)...')
    edgelist = '../weighted_edgelist/edgelist.txt'
    adj_matrix = generate_adjacency_matrix(edgelist)
    dist_dict = generate_distance_dict(adj_matrix)
    sorted_dist_dic = OrderedDict(sorted(dist_dict.items(), key=operator.itemgetter(1)))


    communities = [None]
    char_count = 6486
    for i in range(1, char_count+1):
        communities.append(Community(i, i, True))

    print('Searching Communities, Please Wait...')
    hierarchical_clustering(communities, sorted_dist_dic, adj_matrix)


    community_output = {}
    for i in range(1, len(communities)):
        if communities[i].comm_id not in community_output:
            community_output[communities[i].comm_id] = [communities[i]]
        else:
            community_output[communities[i].comm_id].append(communities[i])

    # sorted_output = OrderedDict(sorted(community_output.items(), key=lambda t: (t[0], len(t[1])), reverse=True))

    print('Generating Output, Please Wait...')
    txt_output = ''
    for out in community_output.items():
        if len(out[1]) > 10:
            msg = '\n********** Community [{}] ************\n'.format(out[0])
            txt_output += msg
            for node in out[1]:
                txt_output += node.__repr__()

    with codecs.open('../outputs/HierarchicalClusteringCommunities.txt', 'w', encoding='utf-8', errors='ignore') as file:
        file.write(txt_output)

main()
