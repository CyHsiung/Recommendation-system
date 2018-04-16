from os.path import join
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import LinearRegression as LR
# from sklearn.svm import SVR
from collections import OrderedDict

from metapath2vec.meta2vec import meta2vec
from metapath2vec.meta2vecHIN import *
from Utils.LR_helper import *
from PPR import *
from HIN.train import train_neural_network
from HIN.predict import predict


def evaluation(G, df_pref, df_tag, df_table, feature_type, args):
	clf = RandomForestRegressor(random_state=42, n_jobs=-1)
	# clf = LR(n_jobs=-1)
	# clf = SVR()

	# def removed_edge(graph, df_pref, df_table, drop_pre_thr = 30, drop_user_rate = 0.3, drop_pre_rate = 0.3):
	print("removing edges from graph")
	G, removed_pre, IDCG, item_num = removed_edge(G, df_pref, df_table, 1, 0.3, 0.1, args.graph_type)

	if feature_type == 'PPR' or feature_type == 'meta2vec':
		if feature_type == 'PPR':
			print("PPR feature generating")
			user_feature, item_feature = PPR_feature_generator(G, args.tol, args.maxIter, 0.85, args.graph_type)
			# user_feature, item_feature = np.zeros((10, 502)), np.zeros((36, 502))
			print('user shape:', user_feature.shape, 'item shape:', item_feature.shape)
			print("generating training data")
			x_train, y_train, x_test, y_test = generate_data(user_feature, item_feature, G, removed_pre, df_pref, df_table, args.graph_type)
		elif feature_type == 'meta2vec':
			n = G.getCount()

			print("meta2vec feature generating")
			user_feature, item_feature, _ = meta2vec(nodeById = G.NodeList, userNum = n[0], prodNum = n[2], args = args)
			# user_feature, item_feature = np.zeros((10, 100)), np.zeros((376, 200))

			print('user shape:', user_feature.shape, 'item shape:', item_feature.shape)
			print("generating training data")
			x_train, y_train, x_test, y_test = generate_data(user_feature, item_feature, G, removed_pre, df_pref, df_table, args.graph_type)		
	

		# Save np array
		from os.path import join
		print(args.corpus_dir)
		print(args.graph_name)
		print(str(args.maxIter))

		a = join(args.corpus_dir, "PPR")
		np.save(join(args.corpus_dir, "PPR", args.graph_name + "_" + str(args.maxIter) + "_x_train.npy"), x_train)
		np.save(join(args.corpus_dir, "PPR", args.graph_name + "_" + str(args.maxIter) + "_y_train.npy"), y_train)
		np.save(join(args.corpus_dir, "PPR", args.graph_name + "_" + str(args.maxIter) + "_x_test.npy"), x_test)
		np.save(join(args.corpus_dir, "PPR", args.graph_name + "_" + str(args.maxIter) + "_y_test.npy"), y_test)
		

		# manuipolation
		x_train = manipulate(x_train)
		# y_train = manipulate(y_train)
		x_test = manipulate(x_test)
		# y_test = manipulate(y_test)


		print("training the model")
		clf.fit(x_train, y_train)

		print("predicting")
		y_predict = clf.predict(x_test)



	elif feature_type == 'HIN':
		print("generating training data")
		n = G.getCount()
		user_feature, item_feature = meta2vecHIN(nodeById = G.NodeList, userNum = n[0], prodNum = n[2], args = args)
		
		print("Hin training data combinding")
		total_x_train, total_y_train, val_x, val_y, total_x_test, total_y_test = hin_generate_data(user_feature, item_feature, 0.8, G, removed_pre, df_pref, df_table, args.graph_type)



		train_neural_network(total_x_train, total_y_train, val_x, val_y)

		y_predict = predict(total_x_test, total_y_test)


	offset = 0
	DCG = []
	base_DCG = []
	for item_per_user in item_num:
		y_user = y_predict[offset:offset + item_per_user]							# extract user's data
		if args.feature_type == 'PPR' or args.feature_type == 'meta2vec':
			if args.graph_type == 'w':
				rate_user = y_test[0][offset:offset + item_per_user]
			else:
				rate_user = y_test[1][offset:offset + item_per_user]
				
		elif args.feature_type == 'HIN':
			rate_user = np.asarray(total_y_test[offset:offset + item_per_user])

		# Find the order for these
		idx_sorted = sorted(range(len(y_user)), key = lambda i: -y_user[i])		# find the order 
		rate_list = rate_user[idx_sorted]										# find the rate order
		DCG.append(DCG_calculator(rate_list))									# find the DCG of this user
		base_DCG.append(DCG_calculator(sorted(rate_list)))
		offset += item_per_user													# update offset
		print(rate_list)

	# Evaluate the model
	print("evaluating")
	score = 0
	n = len(DCG)
	for dcg, idcg, base_dcg in zip(DCG, IDCG, base_DCG):
		score += (dcg - base_dcg) / (idcg - base_dcg)

	score /= n

	print('Testing score = ', score)
