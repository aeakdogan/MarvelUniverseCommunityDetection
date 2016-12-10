import codecs
import operator

char_count = 0
comic_count = 0

chars = [None] * 10000
comics = [None] * 20000
counts = {}
outputFile = open('outputs/charCounts.txt', 'w+')
with codecs.open("inputs/porgat.txt", 'r', encoding='utf-8', errors='ignore') as file:
    line_count = 0

    for line in file:
        if line_count == 0:
            tmp = line.split(' ')
            char_count = int(tmp[2])
            comic_count = int(tmp[1]) - char_count
        elif line_count <= char_count + comic_count:
            tmp = line.split(' ', 1)
            if line_count <= char_count:
                tmp[1] = tmp[1].split('"')[1::2][0]
                #print('char id: ', tmp[0], 'char name: ', tmp[1])
                chars[int(tmp[0])] = tmp[1]
            else:
                tmp[1] = tmp[1].split('"')[1::2][0]
                #print('comic id: ', tmp[0], 'comic name: ', tmp[1])
                comics[int(tmp[0])] = tmp[1]
        elif line_count != char_count + comic_count + 1:
            tmp = line.split(' ')
            char = int(tmp[0])
            cnt = len(tmp) - 1
            #for comic in tmp[1:]:
            #    counts[char] += 1

            if char in counts:
                counts[char] += cnt
            else:
                counts[char] = cnt
        line_count += 1


print('comic count: ', comic_count, file=outputFile)
print('char count: ', char_count, file=outputFile)

counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)

print("{0:4} {1:30} {2}".format('ID', 'Name', 'Count'), file=outputFile)
for char in counts:
    print("{0:4} {1:30} {2}".format(char[0], chars[char[0]], char[1]), file=outputFile)
