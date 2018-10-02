import sys
import re
import random

INF = 0X7fffffff
STOP_WORDS = ['and', 'a', 'the', 'to', 'from', 'this', 'that', 'is', 'are', 'in', 'on', 'by', 'these', 'of', 'it', 'its', 'for']
B = 6
R = 20
S = 0.91

def parser(line):       
    pair = line.split(' ', 1)
    words = re.split(r'\s+', re.sub(r'[^a-zA-Z ]+', '', pair[1]))
    for i in range(len(words)):
    	words[i] = words[i].lower()
    return (pair[0], words)

def parser2(line):    
    
    pair = line.split(' ', 1)
    words = re.split(r'\s+', re.sub(r'[^a-zA-Z]+', '', pair[1]))
    for i in range(len(words)):
    	words[i] = words[i].lower()
    return (pair[0], words)

def is_prime(n):
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False

        return True
def get_c(n):
    if is_prime(n):
        return n
    else:
        return get_c(n + 1)
	

def get_sim(pair):
	count = 0
	for i in range(B * R):
		if sig_mat[pair[0]][i] == sig_mat[pair[1]][i]:
			count += 1
	return count


input_file = open(sys.argv[1], 'r')

documents = []
shingles = []

"""
#code using parser2(character based shingle)
for line in input_file:
	parsed = parser2(line)
	line_shingles = []
	for i in range(len(parsed[1][0]) - 2):
		shingle = parsed[1][0][i: i + 3]
		line_shingles.append(shingle)
		if not shingle in shingles:
			shingles.append(shingle)
	documents.append((parsed[0], line_shingles))

"""
#code using parser(word based shingle)
for line in input_file:
	parsed = parser(line)
	line_shingles = []
	for i in range(len(parsed[1]) - 2):
		if parsed[1][i] in STOP_WORDS:
			shingle = parsed[1][i:i + 3]
			line_shingles.append(shingle)
			if not shingle in shingles:
				shingles.append(shingle)
	documents.append((parsed[0], line_shingles))

print(len(shingles))

char_mat = [[0 for i in range(len(documents))] for i in range(len(shingles))]

for i in range(len(shingles)):
	for j in range(len(documents)):
		if shingles[i] in documents[j][1]:
			char_mat[i][j] = 1

sig_mat = [[INF for i in range(B * R)] for i in range(len(documents))]

c = get_c(len(shingles))

print(c)

for k in range(B * R):
	hash_mat = [0 for y in range(len(shingles))]
	a = random.randrange(0, c, 1)
	b = random.randrange(0, c, 1)

	for x in range(len(shingles)):
		hash_mat[x] = (a * x  + b) % c

	for i in range(len(shingles)):
		for j in range(len(documents)):
			if char_mat[i][j] == 1:
				sig_mat[j][k] = min(sig_mat[j][k], hash_mat[i])

candidate_pairs = []

for i in range(B):
	for j in range(len(sig_mat)):
		for k in range(len(sig_mat)):
			if j < k and sig_mat[j][R * i:R * (i + 1)] == sig_mat[k][R * i:R * (i + 1)] and not (j, k) in candidate_pairs:
				candidate_pairs.append((j, k))

for pair in candidate_pairs:
	count = get_sim(pair)
	if count >= B * R * S:
		print("%s\t%s\t%f" %(documents[pair[0]][0], documents[pair[1]][0], count/float(B * R)))	

input_file.close()

#parser2
#7min 7sec using 3 character shingle(10242 shingles)
#output
#t8413   t269    1.000000
#t1621   t7958   1.000000
#t448    t8535   1.000000
#t980    t2023   0.983333
#t3268   t7998   0.991667

#parser
#32min using 3 word shingle with stop words(82801 shingles)
#output

#t8413   t269    1.000000
#t3268   t7998   0.975000
#t1621   t7958   1.000000
#t448    t8535   1.000000
#t980    t2023   0.950000
