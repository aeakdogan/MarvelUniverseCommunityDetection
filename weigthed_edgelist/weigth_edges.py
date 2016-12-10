import codecs
import collections
import operator

filepath = 'edgelist.txt'
book_char_dict = {}
with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        linesplit = line.split()
        x = int(linesplit[0])
        y = [int(num) for num in linesplit[1:]]
        for cbook in y:
            if cbook not in book_char_dict:
                book_char_dict[cbook] = [x]
            else:
                book_char_dict[cbook].append(x)


edge_dict = {}
for item in book_char_dict.items():
    # print(type(item), item[0], item[1])
    cbook = item[0]
    characters = item[1]
    for idx1 in range(len(characters)):
        for idx2 in range(idx1+1, len(characters)):
            if (characters[idx1], characters[idx2]) not in edge_dict:
                edge_dict[(characters[idx1], characters[idx2])] = 1
            else:
                weight = edge_dict[(characters[idx1], characters[idx2])]
                edge_dict[(characters[idx1], characters[idx2])] = weight + 1

# Sort edges by weights
sorted_edges = collections.OrderedDict(sorted(edge_dict.items(), key=operator.itemgetter(1), reverse=True))

#Output weighted edges
lines = ['vertex1, vertex2, weight\n']
for item in sorted_edges.items():
    vertex1 = item[0][0]
    vertex2 = item[0][1]
    weight = item[1]
    line = '{}, {}, {}\n'.format(vertex1, vertex2, weight)
    lines.append(line)

outputpath = 'weighted_edges.txt'
with codecs.open(outputpath, 'w', encoding='utf-8', errors='ignore') as file:
    file.writelines(lines)




