import numpy as np
from scipy.sparse import lil_matrix
from numpy import array
from scipy.sparse.linalg import norm
from tqdm import tqdm

def buildAMatrix(graph, graph_type):

	n = graph.getCount()

	if graph_type == 'w':
		type_list = ['next_user', 'next_pref', 'next_prod', 'next_tags']
	else:
		type_list = ['next_user', 'next_prod', 'next_tags']

	n = np.cumsum(n)
	# print(n)

	M = lil_matrix((n[-1], n[-1]))

	for key in tqdm(graph.NodeList):
		row_idx = getIndex(key, n)
		node = graph.NodeList[key]
		
		key_list = []
		col_idx = []

		for type_next in type_list:
			key_list.extend(node[type_next])

		for key2 in key_list:
			col_idx.append(getIndex(key2, n))

		# print(col_idx)
		if len(col_idx) > 0:
			M[row_idx, col_idx] = 1/len(col_idx)

	# print(M.toarray())
	return M

def getIndex(key,n):
	idx = -1
	if "user_" in key:
		idx = 0
	elif "pref_" in key:
		idx = n[0]
	elif "product_U" in key:
		idx = n[1]
	elif "product_D" in key:
		idx = n[2]
	elif "tags_U" in key:
		idx = n[3]
	elif "tags_D" in key:
		idx = n[4]
	else:
		print(key)
		print("splitting error")


	idx += int(key.split("_")[-1])

	return idx

def PPR_calculator(M, tol, maxIter, beta, e):
	n = M.shape[0]
	r = lil_matrix((n,1))
	r_pre = r.copy()
	r_pre[0] = 1
	iterCnt = 0

	while norm(r - r_pre)/np.sqrt(r.shape[0]) > tol and iterCnt < maxIter:
		r_pre = r
		r = beta * M * r + (1 - beta) * e
		iterCnt += 1

	if iterCnt == maxIter:
		print("iter Max")

	return r

def feature_getter(r, n):
	m = n[-1]
	d = np.ndarray.flatten(r[-m:,0].toarray())
	u = np.ndarray.flatten(r[-2*m:-m,0].toarray())
	with np.errstate(divide='ignore', invalid='ignore'):
		res = d/u
		res[np.isnan(res)] = 0

	return res

def PPR_feature_generator(graph, tol, maxIter, beta, graph_type):
	print("creating sparse matrix")
	M = buildAMatrix(graph, graph_type)
	
	n = graph.getCount()


	print("generating user feature:")
	user_feature = []
	for idx in tqdm(range(n[0])):		# loop through all user
		e = lil_matrix((M.shape[0], 1))
		e[idx] = 1 
		r = PPR_calculator(M, tol, maxIter, beta, e)

		user_feature.append(feature_getter(r, n))

	print("generating item feature")
	n_cum = np.cumsum(n)
	item_feature = M[n_cum[1]:n_cum[1]+n[2], n_cum[3]:n_cum[3]+n[4]]
	item_feature[item_feature>0] = 1

	# print('user shape:', np.asarray(user_feature).shape, 'item shape:', item_feature.shape)
	return np.asarray(user_feature), item_feature.toarray()
