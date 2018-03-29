import sys
import re
import pandas as pd
from os.path import join
from tqdm import tqdm

tagFileName = 'tags.txt'
prefFileName = 'preference.txt'
corpus_dir = './corpus'
inputFileName = 'amazon-meta.txt'

cnt = 0

p_tag = re.compile('[[]\d+[]]')
p_customer = re.compile('cutomer:\s+\w+')
p_rate = re.compile('rating:\s\d+')
p_review = re.compile('downloaded:\s\d+')

cate_cnt = 0
cate = False
tags_set = set()
review_cnt = 0
review = False

fw_tag = open(join(corpus_dir, tagFileName), 'w')
fw_pref = open(join(corpus_dir, prefFileName), 'w')

fw_tag.write("product\ttag\n")
fw_pref.write("user\tproduct\trating\n")

fr = open(join(corpus_dir, inputFileName), 'r')
print('preprocessing start')
lines = fr.readlines()
for line in tqdm(lines):
	line = line.strip()
	if cate:
		cate_cnt -= 1
		raw_tags = p_tag.findall(line)
		for tags in raw_tags:
			tags_set.add(tags[1:-1])

		if cate_cnt <= 0:
			cate = False
			tags = ','.join(list(tags_set))		
			fw_tag.write('%s\t%s\n' % (key, tags)) 
			tags_set = set()
		continue

	if review:
		review_cnt -= 1
		customer_id = p_customer.findall(line)[0].split()[-1]
		rate = p_rate.findall(line)[0].split()[-1]

		fw_pref.write('%s\t%s\t%s\n' % (customer_id, key, rate)) 

		if review_cnt <= 0:
			review = False


	if line == "":
		cnt += 1
		# if cnt % 100 == 0:
		# 	print(cnt / 548552 * 100, '%')

		continue

	if line.startswith('Id:'):
		key = line.split()[-1]
		continue

	if line.startswith('categories:'):
		cate_cnt = int(line.split()[-1])
		cate = True
		continue

	if line.startswith('reviews:'):
		review_cnt = int(p_review.findall(line)[0].split()[-1])
		if review_cnt > 0:
			review = True
		continue

fw_tag.close()
fw_pref.close()

# Merge preference 
print("Merging the preference")
df_pre = pd.read_table(join(corpus_dir, prefFileName))
df_pre = df_pre.groupby(['user', 'product']).agg('mean')
df_pre.to_csv(join(corpus_dir, 'merge_' + prefFileName), sep='\t')
