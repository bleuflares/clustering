import re
import sys
from pyspark import SparkConf, SparkContext

ALPHABET_PAIRS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def intersect(lists):
  intersection = []
  if len(lists) > 1:
    for f in lists[1]:
      if f in lists[0]:
        intersection.append(f)
  return len(intersection)

def mapper(lst):
    return (lst[0], lst[1:])

def match_users(a, b):
    if not a[0] in b[1]:
        count = intersect([a[1], b[1]])
        return ((a[0], b[0]), count)

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
splits = lines.flatMap(lambda l: re.split(r'[^\w]+', l))
splits.map(mapper)
pair_counts = users.reduce(match_users)
pair_counts.saveAsTextFile(sys.argv[2])
sc.stop()