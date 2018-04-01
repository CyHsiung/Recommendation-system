from os.path import join
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from collections import OrderedDict

from metapath2vec.meta2vec import meta2vec
from Utils.LR_helper import *
from PPR import *


def evaluation(G, df_pref, df_tag, df_table, feature_type, args):
	clf = RandomForestRegressor()

	'''
	Tunning Code
	'''
	# m_k = 0
	# m_score = 0

	# # klist = [i for i in range(1,50,1)]
	# klist = [0]
	# for k in klist:
	#     clf = LR(random_state=7,n_estimators=62,max_depth=15)
	#     X_select= X[:,idlist[:292]]
	#     score = cross_val_score(clf,X_select,Y,cv=5).mean()

	#     print('k= ',k,' acc = ',score)
	#     if m_score<score:
	#         m_score = score
	#         m_k = k

	# print('best choise')
	# print('k= ',m_k,' acc = ',m_score)

	# def removed_edge(graph, df_pref, df_table, drop_pre_thr = 30, drop_user_rate = 0.3, drop_pre_rate = 0.3):
	print("removing edges from graph")
	G, removed_pre, IDCG, item_num = removed_edge(G, df_pref, df_table, 1, 0.3, 0.1)

	if feature_type == 'PPR':
		print("PPR feature generating")
		user_feature, item_feature = PPR_feature_generator(G, 1e-8, 100, 0.85)
		# user_feature, item_feature = np.zeros((10, 502)), np.zeros((36, 502))
	elif feature_type == 'meta2vec':
		n = G.getCount(False)

		print("meta2vec feature generating")
		user_feature, item_feature, _ = meta2vec(nodeById = G.NodeList, userNum = n[0], prodNum = n[2], args = args)
		# user_feature, item_feature = np.zeros((10, 100)), np.zeros((376, 200))

	print('user shape:', user_feature.shape, 'item shape:', item_feature.shape)



	

	print("generating training data")
	x_train, y_train, x_test, y_test = generate_data(user_feature, item_feature, G, removed_pre, df_pref, df_table)


	print("training the model")
	clf.fit(x_train, y_train)

	print("predicting")
	predict = clf.predict(x_test)

	offset = 0
	DCG = []
	for item_per_user in item_num:
		y_user = predict[offset:offset+item_per_user]							# extract user's data
		rate_user = y_test[offset:offset+item_per_user]

		# Find the order for these
		idx_sorted = sorted(range(len(y_user)), key = lambda i:-y_user[i])		# find the order 
		rate_list = rate_user[idx_sorted]										# find the rate order
		DCG.append(DCG_calculator(rate_list))									# find the DCG of this user
		offset += item_per_user													# update offset
		print(rate_list)

	# Evaluate the model
	print("evaluating")
	score = 0
	n = len(DCG)
	# print(DCG)
	# print(IDCG)
	for dcg, idcg in zip(DCG, IDCG):
		score += dcg / idcg

	score /= n

	print('Testing score = ', score)
