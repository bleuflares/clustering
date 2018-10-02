import sys
import re
file = open(sys.argv[1])
arr = []
for line in file:
    friends = re.split(r'[^\w]+', line)
    arr.append(friends)

count = 0
for idx1 in arr:
	for idx2 in arr:
		if idx1 != idx2:
			for item1 in idx1:
				for item2 in idx2:
					if item1 ==item2:
						count += 1
print(count)