import pandas as pd
from os.path import join

tagFileName = 'tags.txt'
prefFileName = 'merge_preference.txt'
corpus_dir = './data'


user_num = 10

df_tag = pd.read_table(join(corpus_dir, tagFileName))
df_pre = pd.read_table(join(corpus_dir, prefFileName))


print('tags table')
print(df_tag.head())
print('pre table')
print(df_pre.head())

product_set = set()

# user_series = df_pre.user.sample.unique().sample(user_num)
# print(df_pre.groupby('user').agg('count').sort_values(by = 'product').head(5))
df_pre_num = df_pre.groupby('user').size().reset_index(name='counts')
print(df_pre_num[(df_pre_num.counts >= 3) & (df_pre_num.counts <= 5)].sample(user_num,random_state = 12))
userlist = df_pre_num[(df_pre_num.counts >= 3) & (df_pre_num.counts <= 5)].sample(user_num,random_state = 12).user

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


df_toy_tag.to_csv(join(corpus_dir, 'toy_tags.txt'), sep='\t', index = False)
df_toy_pre.to_csv(join(corpus_dir, 'toy_preference.txt'), sep='\t', index = False)

"""code for merging """
# df_pre = df_pre.groupby(['user', 'product']).agg('mean')
# print(df_pre.head(5))
# df_pre.to_csv(join(corpus_dir, 'merge_' + prefFileName), sep='\t')