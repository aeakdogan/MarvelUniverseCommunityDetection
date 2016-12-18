import codecs

import time

edges = {}
sumOfWeights = []
isInCommunity = []
belongingDegrees = []
neighborsOfCommunity = []


def findMaxWeightedEdge(edges_list):
    maxWeighedEdge = 0
    vertex1 = -1
    vertex2 = -1
    for edge in edges_list:
        if maxWeighedEdge < edge[2]:
            maxWeighedEdge = edge[2]
            vertex1 = edge[0]
            vertex2 = edge[1]
    return [vertex1, vertex2]


def findMaxBelongingDegreedNode(c):
    global neighborsOfCommunity
    maxBelongingDegree = 0
    maxBelongingDegreedNode = -1
    for node in neighborsOfCommunity:
        if belongingDegrees[node] / sumOfWeights[node] > maxBelongingDegree:
            maxBelongingDegree = belongingDegrees[node] / sumOfWeights[node]
            maxBelongingDegreedNode = node
    return maxBelongingDegreedNode


def detectionAlgorithm(n, edges_list):
    communities = []
    global isInCommunity
    global belongingDegrees
    global neighborsOfCommunity

    while len(edges_list) > 0:
        c = findMaxWeightedEdge(edges_list)
        isInCommunity = [False] * (n + 1)
        belongingDegrees = [0] * (n + 1)
        neighborsOfCommunity = []
        weightOfCuttingEdgesOfCommunity = 0
        weightOfAllEdgesOfCommunity = 0

        isInCommunity[c[0]] = True
        isInCommunity[c[1]] = True
        for node in edges[c[0]]:
            if node[0] not in neighborsOfCommunity and not isInCommunity[node[0]]:
                neighborsOfCommunity.append(node[0])
            if node[0] < c[0] or not isInCommunity[node[0]]:
                weightOfAllEdgesOfCommunity += node[1]
            if node[0] in neighborsOfCommunity:
                weightOfCuttingEdgesOfCommunity += node[1]
            belongingDegrees[node[0]] += node[1]
        for node in edges[c[1]]:
            if node[0] not in neighborsOfCommunity and not isInCommunity[node[0]]:
                neighborsOfCommunity.append(node[0])
            if node[0] < c[1] or not isInCommunity[node[0]]:
                weightOfAllEdgesOfCommunity += node[1]
            if node[0] in neighborsOfCommunity:
                weightOfCuttingEdgesOfCommunity += node[1]
            belongingDegrees[node[0]] += node[1]

        if len(neighborsOfCommunity) > 0:
            while True:
                new_node = findMaxBelongingDegreedNode(c)
                if new_node == -1:
                    break
                new_c = c + [new_node]

                currentConductance = weightOfCuttingEdgesOfCommunity / weightOfAllEdgesOfCommunity
                newCuttingWeight = weightOfCuttingEdgesOfCommunity
                newAllWeight = weightOfAllEdgesOfCommunity

                for node in edges[new_node]:
                    if isInCommunity[node[0]]:
                        newCuttingWeight -= node[1]
                    else:
                        newCuttingWeight += node[1]
                    newAllWeight += node[1]
                newConductance = newCuttingWeight / newAllWeight

                if newConductance < currentConductance:
                    c = new_c
                    weightOfCuttingEdgesOfCommunity = newCuttingWeight
                    weightOfAllEdgesOfCommunity = newAllWeight

                    isInCommunity[new_node] = True
                    for node in edges[new_node]:
                        belongingDegrees[node[0]] += node[1]
                        if node[0] not in neighborsOfCommunity and not isInCommunity[node[0]]:
                            neighborsOfCommunity.append(node[0])
                    neighborsOfCommunity.remove(new_node)
                else:
                    break

        # print([chr(ord('a') + node - 1) for node in c])
        communities.append(c)
        tmp_list = []
        for edge in edges_list:
            if not isInCommunity[edge[0]] or not isInCommunity[edge[1]]:
                tmp_list.append(edge)
        edges_list = tmp_list
    return communities


def main():
    edges_list = []
    line_count = 0
    n = 0
    outputFile = open('../outputs/communities.txt', 'w+')
    with codecs.open("../inputs/sampleInput.txt", 'r', encoding='utf-8', errors='ignore') as file:
    #with codecs.open("../inputs/weighted_edges.txt", 'r', encoding='utf-8', errors='ignore') as file:
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

            edges_list.append([vertex1, vertex2, weight])
            line_count += 1
    for i in range(1, n + 1):
        if i not in edges:
            edges[i] = []

    sumOfWeights.append(0)
    for i in range(1, n + 1):
        sumOfWeights.append(0)
        for node in edges[i]:
            sumOfWeights[i] += node[1]

    communities = detectionAlgorithm(n, edges_list)

    cnt = 1
    for community in communities:
        print(cnt, community, file=outputFile)
        cnt += 1


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
