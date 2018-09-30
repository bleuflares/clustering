import sys

input_file = open(sys.argv[1], 'r')
s = 100 #support value
session_list = []
item_dict = {}
for line in input_file:
	item_list = line.split()
	for item in item_list:
		dict_item = item_dict.get(item)
		if dict_item == None:
			item_dict[item] = 1
		else:
			item_dict[item] = dict_item + 1
	session_list.append(item_list)

frequent_items = []
dict_keys = item_dict.keys()
for key in dict_keys:
	if item_dict[key] >= s:
		frequent_items.append(key)

candidate_pairs = [0 for i in range(len(frequent_items) * len(frequent_items))]
for session in session_list:
	for item1 in session:
		for item2 in session:
			if item1 != item2 and item1 in frequent_items and item2 in frequent_items:
				pair_index = frequent_items.index(item1) * len(frequent_items) + frequent_items.index(item2)
				if frequent_items.index(item1) < frequent_items.index(item2):
					candidate_pairs[pair_index] = candidate_pairs[pair_index] + 1

frequent_pairs_count = 0
frequent_pairs = []
for i in range(len(candidate_pairs)):
	if candidate_pairs[i] > s:
		frequent_pairs_count += 1

top_10_indices = sorted(range(len(candidate_pairs)), key=lambda i: candidate_pairs[i])[-10:]

top_10 = []
for index in top_10_indices:
	x = frequent_items[index / len(frequent_items)]
	y = frequent_items[index % len(frequent_items)]
	top_10.append(sorted((x, y)))
top_10.sort(key=lambda tup: tup[0], reverse=True)

output_file = open(sys.argv[2], 'w')
output_file.write("%d\n" %len(frequent_items))
output_file.write("%d\n" %frequent_pairs_count)
for element in top_10:
	output_file.write("%s\t%s\n" %(element[0], element[1]))
input_file.close()
output_file.close()
