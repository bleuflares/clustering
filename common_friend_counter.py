import re
import sys
from pyspark import SparkConf, SparkContext

PURGE = -0xffffffff

def parser(ids):    
    friends = re.split(r'[^\w]+', ids)
    if len(friends) > 1:
        return friends[0], list(friends[1:])

def mark_pairs(items):
    friends = [((items[0], friend), PURGE) for friend in items[1]]
    common_friends = []
    for friend1 in items[1]:
        for friend2 in items[1]:
            if friend1 != friend2:
                common_friends.append(((friend1, friend2), 1))
    return friends + common_friends

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(sys.argv[1])
    line_pairs = lines.map(lambda ids: parser(ids))
    pairs_map = line_pairs.flatMap(mark_pairs)
    map_counts = pairs_map.reduceByKey(lambda a, b: a + b)
    id_pairs = map_counts.filter(lambda (pair, count): count > 0 and pair[0] < pair[1])
    top_10 = id_pairs.takeOrdered(10, key=lambda (pair, count): -count)
    for item in top_10:
        print("%d\t%d\t%d" %(int(item[0][0]), int(item[0][1]), int(item[1])))
    sc.setLogLevel('WARN')
    sc.stop()