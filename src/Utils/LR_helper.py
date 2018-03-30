import numpy as np
import pandas as pd 
import os.path as join
from collections import OrderedDict

# drop_pre_thr = 30				# When # of p-edge > drop_pre_thr, the user become candidate of drop
# drop_user_rate = 0.3			# perform delete on these ratio of candidates (candidate / total usesr)
# drop_pre_rate = 0.3				# the ratio for drop the edge

def removed_edge(graph, df_pref, df_table, drop_pre_thr = 30, drop_user_rate = 0.3, drop_pre_rate = 0.3):
	# copy an object for not modify original graph
	# graph = G.copy()			# not work
	user_num = graph.getCount()[0]
	

	edge_num = []
	for idx in range(user_num):
		pre_cnt = len(graph.NodeList["user_"+str(idx)]['next_pref'])
		if pre_cnt >= drop_pre_thr:
			edge_num.append((pre_cnt, idx))

	edge_num = sorted(edge_num, reverse=True)

	# find the user fit critera
	removed_pre = OrderedDict()
	user_drop_count = min(len(edge_num), int(drop_user_rate * user_num))
	for drop_idx in range(user_drop_count):
		cnt, idx = edge_num[drop_idx]
		user_name = "user_"+str(idx)
		pre_drop_count = int(drop_pre_rate * cnt)
		
		# random select a edge to remove
		length = len(graph.NodeList["user_"+str(idx)]['next_pref'])
		rand_idx = list(np.random.random_integers(0, length-1, pre_drop_count))

		# record and remove the edges
		for i in sorted(rand_idx, reverse = True):
			try:
				removed_edge_name = graph.NodeList[user_name]['next_pref'][i]
				del graph.NodeList[user_name]['next_pref'][i]
				if user_name not in removed_pre:
					removed_pre[user_name] = [removed_edge_name]
				else:
					removed_pre[user_name].append(removed_edge_name)
			except:
				print("removing edges unknown error (didn't be solved)")
				print("length ", length, ", max of rand_idx = ", max(rand_idx), "length of pref", len(graph.NodeList[user_name]['next_pref']))
			


	IDCG = []
	item_num = []
	for user in removed_pre.keys():
		item_set = set()
		for preference in removed_pre[user]:
			line = preference.split("_")
			item_set.add(line[1])
			item_set.add(line[2])

		rating_list = []

		for item in item_set:
			real_idx = find_item_index(item, df_table)
			real_user_name = find_user_name(user, df_table)
			rate = df_pref[(df_pref['user'] == real_user_name) & (df_pref['product'] == int(item))]['rating'].values[0]
			rating_list.append(float(rate)/5)

		# DCG for this item
		IDCG.append(DCG_calculator(sorted(rating_list, reverse = True)))
		item_num.append(len(rating_list)) 

		# print("IDCG rateinglist :", sorted(rating_list, reverse = True))
	return graph, removed_pre, IDCG, item_num

def generate_data(user_feature, item_feature, graph, removed_pre, df_pref, df_table):
	# Generating training data
	print("Generating training data !!!!")
	user_num = graph.getCount()[0]
	x_train, y_train = [], []
	for idx in range(user_num):
		user_name = "user_"+str(idx)
		item_set = set()
		for pref in graph.NodeList[user_name]['next_pref']:
			line = pref.split("_")
			item_set.add(line[1])
			item_set.add(line[2])

		for item in item_set:
			real_idx = find_item_index(item, df_table)
			real_user_name = find_user_name(user_name, df_table)
			rate = df_pref[(df_pref['user'] == real_user_name) & (df_pref['product'] == int(item))]['rating'].values[0]
			x_train.append(np.concatenate([user_feature[idx, :].flatten(), item_feature[real_idx, :].flatten()]))
			y_train.append(float(rate)/5)


	# Generating testing data
	print("Generating testing data !!!!")
	x_test, y_test = [], []

	for user_name in removed_pre.keys():
		item_set = set()
		for pref in removed_pre[user_name]:
			line = pref.split("_")
			item_set.add(line[1])
			item_set.add(line[2])

		for item in item_set:
			real_idx = find_item_index(item, df_table)
			real_user_name = find_user_name(user_name, df_table)
			rate = df_pref[(df_pref['user'] == real_user_name) & (df_pref['product'] == int(item))]['rating'].values[0]
			x_test.append(np.concatenate([user_feature[idx, :].flatten(), item_feature[real_idx, :].flatten()]))
			y_test.append(float(rate)/5)
	
	print(np.asarray(x_train).shape, np.asarray(y_train).shape, np.asarray(x_test).shape, np.asarray(y_test).shape)
	print(removed_pre)
	return np.asarray(x_train), np.asarray(y_train), np.asarray(x_test), np.asarray(y_test)


def find_item_index(item, df_table):
	return int(df_table["old2new"][item].split("_")[-1].split("_")[-1])
	# return int(list(df_table[df_table["orginal id"] == item]["new id"])[0].split("_")[-1])

def find_user_name(user_name, df_table):
	return df_table["new2old"][user_name]
	# return df_table[df_table["new id"] == user_name]['orginal id'].values[0]

def DCG_calculator(rating_list):
	res = 0
	for i, rate in enumerate(rating_list, 1):
		res += (2**rate - 1) / (np.log2(i+1))

	return res
		
