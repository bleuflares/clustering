import re
import sys
from pyspark import SparkConf, SparkContext

PURGE = -0xffffffff

# parser parses each line of ids to (id, friends list) pair
def parser(ids):
    friends = re.split(r'[^\w]+', ids)
    if len(friends) > 1:
        return friends[0], list(friends[1:])

# mark_pairs is a mapper function that maps each (id1, friends list) to two kinds of key-value pair.
# key of the pairs is all (id1, id2) pair.
# the first kind is ((id1, id2), 1) where id1 and id2 are one of the member of friends list and there is no guarantee that id1 and id2 are not friends.
# the second kind is ((id1, id2), PURGE) where id1 and id2 are friends. This pair is needed to remove the pair of the first kinds whose id1 and id2 are friends.
# The PURGE value will make the value after reduce to be negative and we can later filter it.
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
    line_pairs = lines.map(lambda ids: parser(ids)) #map to generate pair for each line
    pairs_map = line_pairs.flatMap(mark_pairs) #flatMap to generate key-value pair
    map_counts = pairs_map.reduceByKey(lambda a, b: a + b) #reducer to combine the values with equal keys
    id_pairs = map_counts.filter(lambda (pair, count): count > 0 and pair[0] < pair[1]) #filter to remove pairs who are friends and remove duplicates
    top_10 = id_pairs.takeOrdered(10, key=lambda (pair, count): -count) #get the top 10 value as list
    for item in top_10:
        print("%d\t%d\t%d" %(int(item[0][0]), int(item[0][1]), int(item[1])))
    sc.setLogLevel('WARN')
    sc.stop()