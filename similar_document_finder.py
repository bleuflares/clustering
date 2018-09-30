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
    return (pair[0], words.lower())

def is_prime(n):
	i = 2
	while i < n:
		i += 1
		if n % i == 0:
			return False
	return True

def get_c(n):
	while not is_prime(n):
		n += 1
	return n

def check_sim(x, y):
	for i in range(B * R):
		if sig_mat[x][i] == sig_mat[y][i]:
			count += 1
	if count >= B * R * S:
		return True
	else:
		return False


file = open(sys.argv[1], 'r')

documents = []
shingles = []
for line in file:
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
	for i in range(len(parsed[1])- 2):
		shingle = parsed[1][i: i + 2]
		line_shingles.append(shingle)
		if not shingle in shingles:
			shingles.append(shingle)
		documents.append((parsed[0], line_shingles))

char_mat = ([0] * len(documents)) * len(shingles)

for i in range(len(shingles)):
	for j in range(len(documents)):
		if shingles[i] in documents[j][1]:
			char_mat[i][j] = 1

sig_mat = ([INF] * (B * R)) * len(documents)

c = get_c(len(shingles))
for k in range(B * R):
	hash_mat = [0] * len(shingles)
	a = random.radrange(0, c)
	b = random.radrange(0, c)

	for x in range(len(shingles)):
		hash_mat[x] = (a * x  + b) % c

	for i in range(len(shingles)):
		for j in range(len(documents)):
			if char_mat[i][j] == 1:
				sig_mat[j][k] = min(sig_mat[j][k], hash_mat[i])

candidate_pairs = []
for i in range(B):
	band = sig_mat[R * i : R * (i + 1) - 1]
	for j in range(len(band)):
		for k in range(len(band)):
			if j < k and band[j] == band[k] and not (j, k) in candidate_pairs:
				candidate_pairs.append((j, k))

similar_pairs = []

for pair in candidate_pairs:
	if check_sim(pair):
		similar_pairs.append(pair)

print(similar_pairs)
