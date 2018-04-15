# def import_graph(tag_filename, pref_filename):
# 	df_tag = readData(tag_filename)
# 	df_pref = readData(pref_filename)
	
# 	G = TriGraph(df_tag, df_pref)
# 	# G.buildNodeList() -> remove user without neighbors
# 	# G.buildNodeList(False) -> do not remove user without neighbors
# 	G.buildNodeList()
# 	return G.NodeList

from graphProcessing.BuildGraph import *
from graphProcessing.BuildGraphWoPref import *
from graphProcessing.ReadWrite import *
from LR import *
import pandas as pd
from os.path import join
import os
import argparse
import json
import time




project_dir = os.path.abspath('./')
corpus_dir = join(project_dir, 'corpus')

# def buildGraph(corpus_dir, pref_filename, tag_filename):
# 	print("reference loading")
# 	df_tag = readData(join(corpus_dir, tag_filename))
# 	df_pref = readData(join(corpus_dir, pref_filename))

# 	print("building the graph")
# 	G = TriGraph(df_tag, df_pref)
# 	G.buildNodeList(False)

# 	df_table = G.buildMapping()

# 	# dump typeMap.txt
# 	print("dumping the typeMap.txt")
# 	f = open(join(corpus_dir, 'typeMap.txt'),'w')
# 	for key in G.dict:
# 		f.write(key + ' ' + key[:4] + '\n')


# 	return G, df_pref, df_tag, df_table

def loadGraph(corpus_dir, pref_filename, tag_filename, graph_name, graph_type):
	print("reference loading")
	df_tag = readData(join(corpus_dir, tag_filename))
	df_pref = readData(join(corpus_dir, pref_filename))
	# df_table = pd.read_csv(join(corpus_dir, 'table.csv'))
	with open(join(corpus_dir, graph_name+'_table.json')) as fin:
		df_table = json.load(fin)


	print("loading the graph from graph_name = ", graph_name)
	G = readGraph(graph_name, graph_type)

	return G, df_pref, df_tag, df_table

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--feature_type', type=str, default='meta2vec',
                       help='Feature type of evaluation')
	parser.add_argument('--prefFileName', type=str, default='toy_preference.txt',
                       help='preference file name')
	parser.add_argument('--tagFileName', type=str, default='toy_tags.txt',
					   help='tags file name')
	parser.add_argument('--graph_name', type=str, default='graph',
					   help='graph_name')
	parser.add_argument('--graph_type', type=str, default='w',
                       help='graph_type')
	parser.add_argument('--corpus_dir', type=str, default='./corpus',
                       help='Data directory')


	####### PPR-argmument
	parser.add_argument('--maxIter', type=int, default=10000,
					   help='tags file name')
	parser.add_argument('--tol', type=float, default=1e-8,
					   help='graph_name')


	####### semi-argmument
	parser.add_argument('--walks',type=str,default = join(corpus_dir, 'random_walk.txt'), help='text file that has a random walk in each line. A random walk is just a seaquence of node ids separated by a space.')
	parser.add_argument('--types',type=str,default = join(corpus_dir, 'typeMap.txt'), help='text file that has node types. each line is "node id <space> node type"')
	parser.add_argument('--epochs',type=int,default = 10, help='number of epochs')
	# parser.add_argument('--batch',type=int,default=1, help='Batch size.Only batch one is supported now...')
	parser.add_argument('--lr',type=float,default=0.01, help='learning rate')
	parser.add_argument('--log', default = join(corpus_dir, './log'),type=str,help='log directory')
	parser.add_argument('--log-interval',default=-1,type=int,help='log intervals. -1 means per epoch')
	parser.add_argument('--max-keep-model',default=10,type=int,help='number of models to keep saving')
	parser.add_argument('--embedding-dim',default = 100,type=int,help='embedding dimensions')
	parser.add_argument('--negative-samples',default = 5,type=int,help='number of negative samples')
	parser.add_argument('--care-type',default = 0,type=int,help='care type or not. if 1, it cares (i.e. heterogeneous negative sampling). If 0, it does not care (i.e. normal negative sampling). ')
	parser.add_argument('--window',default = 3,type=int,help='context window size')

	parser.add_argument('--stepInEachPath',default = 20,type=int,help='step in each random walk path')
	parser.add_argument('--trainOrTest',default = 'train',type=str,help='train / test')



	args = parser.parse_args()
	# modify for multiple graph running
	args.types = join(corpus_dir, args.graph_name+"_typeMap.txt")

	G, df_pref, df_tag, df_table = loadGraph(args.corpus_dir, args.prefFileName, args.tagFileName, args.graph_name, args.graph_type)

	# for key, value in df_table['old2new']['item_U'].items():
	# 	print(key, value)


	evaluation(G, df_pref, df_tag, df_table, args.feature_type, args)


if __name__ == '__main__':
	start_time = time.time()
	main()
	print("--- %s seconds ---" % (time.time() - start_time))
