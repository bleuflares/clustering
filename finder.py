import re
import sys
from pyspark import SparkConf, SparkContext

BUFVAL = -0xffffffff

def parser(ids):    
    friends = re.split(r'[^\w]+', ids)
    if len(friends) > 1:
        return friends[0], list(friends[1:])
def mark_pairs(items):
    friends = [((items[0], friend), BUFVAL) for friend in items[1]]
    common_friends = []
    for friend1 in items[1]:
        for friend2 in items[1]:
            if friend1 != friend2:
                common_friends.append(((friend1, friend2), 1))
    return friends + common_friends

def pair_to_list(sorted_pairs):
    return [sorted_pairs[0][0], sorted_pairs[0][1], sorted_pairs[1]]

def write_to_file(content, filename):
    output = open(filename, 'w')
    for item in content:
        output.write("%d\t%d\t%d\n" %(int(item[0][0]), int(item[0][1]), int(item[1])))
    output.close()

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
line_pairs = lines.map(lambda ids: parser(ids))
pairs_map = line_pairs.flatMap(mark_pairs)
map_counts = pairs_map.reduceByKey(lambda a, b: a + b)
id_pairs = map_counts.filter(lambda (pair, count): count > 0)
sorted_pairs = id_pairs.filter(lambda (pair, count): pair[0] < pair[1])
top_10 = sorted_pairs.take(10)
write_to_file(top_10, sys.argv[2])

sc.stop()