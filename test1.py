import sys
import re

def parser(ids):    
    friends = re.split(r'[^\w]+', ids)
    if len(friends) > 1:
        return (friends[0], list(friends[1:]))

file = open(sys.argv[1])

array = [[0 for i in range(50000)] for j in range(50000)]

friends = []
for line in file:
	friends.append(parser(line))

for friend1 in friends:
	for friend2 in friends:
		if not friend1[0] in friend2[1]:
			for a in range(len(friend1[1])):
				for b in range(len(friend2[1])):
					if a < b:
						array[a][b] = array[a][b] + 1

for a in range(50000):
	for b in range(50000):
		if array[a][b] > 90:
			print(a, b, array[a][b])
