import pandas as pd
import argparse
from os.path import join, isfile


def toy_example_builder(user_num, product_range, tagFileName, prefFileName, corpus_dir, output_header):
	df_tag = pd.read_table(join(corpus_dir, tagFileName))
	df_pre = pd.read_table(join(corpus_dir, prefFileName))

	print('tags table')
	print(df_tag.head())
	print('pre table')
	print(df_pre.head())

	product_set = set()

	df_pre_num = df_pre.groupby('user').size().reset_index(name='counts')
	print(df_pre_num[(df_pre_num.counts >= product_range[0]) & (df_pre_num.counts <= product_range[1])].sample(user_num,random_state = 12))
	userlist = df_pre_num[(df_pre_num.counts >= product_range[0]) & (df_pre_num.counts <= product_range[1])].sample(user_num,random_state = 12).user

	print(list(userlist))

	# Cutting the user from the original dataset.

	for idx, user in enumerate(list(userlist)):
		if idx == 0:
			df_toy_pre = df_pre[df_pre.user == user]
		else:
			df_toy_pre = df_toy_pre.append(df_pre[df_pre.user == user])

		productlist = list(df_pre[df_pre.user == user]['product'])
		for product in productlist:
			product_set.add(product)

	for idx, product in enumerate(list(product_set)):
		if idx == 0:
			df_toy_tag = df_tag[df_tag['product'] == product]
		else:
			df_toy_tag = df_toy_tag.append(df_tag[df_tag['product'] == product])


	df_toy_tag.to_csv(join(corpus_dir, output_header + '_tags.txt'), sep='\t', index = False)
	df_toy_pre.to_csv(join(corpus_dir, output_header + '_preference.txt'), sep='\t', index = False)

def pref_merging(corpus_dir):
	df_pre = pd.read_table(join(corpus_dir, ""))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--user_num', type=int, default=10,
                       help='user number you need')
	parser.add_argument('--product_range', type=str, default = '3-5',
					   help='the range of product per user')
	parser.add_argument('--corpus_dir', type=str, default='./corpus',
                       help='Data directory')
	parser.add_argument('--prefFileName', type=str, default='merge_preference.txt',
                       help='preference file name')
	parser.add_argument('--tagFileName', type=str, default='tags.txt',
                       help='tags file name')
	parser.add_argument('--output_header', type=str, default='toy',
                       help='the header of toy example')
	args = parser.parse_args()

	user_num = args.user_num
	product_range = [int(args.product_range.split('-')[0]), int(args.product_range.split('-')[1])]
	tagFileName = args.tagFileName
	prefFileName = args.prefFileName
	corpus_dir = args.corpus_dir
	output_header = args.output_header

	print("extracting toy_example")
	toy_example_builder(user_num, product_range, tagFileName, prefFileName, corpus_dir, output_header)

if __name__ == '__main__':
	main()
	