import sys
import re
import random

INF = 0X7fffffff
#STOP_WORDS = ['and', 'a', 'the', 'to', 'from', 'this', 'that', 'is', 'are', 'in', 'on', 'by', 'these', 'of', 'it', 'its', 'for']
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
for line in input_file:
	"""
	parsed = parser(line)
	shingles = []
	for i in range(len(parsed[1] - 2)):
		if parsed[1][i] in STOP_WORDS:
			shingle = parsed[1][i:i + 2]
			shingles.append(shingle)
			if not shingle in whole_shingles:
				whole_shingles.append(shingle)
	"""
	parsed = parser2(line)
	line_shingles = []
	for i in range(len(parsed[1][0]) - 2):
		shingle = parsed[1][0][i: i + 3]
		line_shingles.append(shingle)
		if not shingle in shingles:
			shingles.append(shingle)
	documents.append((parsed[0], line_shingles))

char_mat = [[0 for i in range(len(documents))] for i in range(len(shingles))]

for i in range(len(shingles)):
	for j in range(len(documents)):
		if shingles[i] in documents[j][1]:
			char_mat[i][j] = 1

sig_mat = [[INF for i in range(B * R)] for i in range(len(documents))]

c = get_c(len(shingles))
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

output_file = open(sys.argv[2], 'w')
for pair in candidate_pairs:
	count = get_sim(pair)
	if count >= B * R * S:
		output_file.write("%s\t%s\t%f\n" %(documents[pair[0]][0], documents[pair[1]][0], count/float(B * R * S)))	

input_file.close()
output_file.close()