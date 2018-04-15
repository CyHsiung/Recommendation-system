from graphProcessing.BuildGraph import *
from graphProcessing.ReadWrite import *
from graphProcessing.BuildGraphWoPref import *

import argparse
from os.path import join
import pandas as pd
import time
start_time = time.time()

def buildGraph(corpus_dir, pref_filename, tag_filename, graph_name, graph_type, pref_type):
	print("reference loading")
	df_tag = pd.read_table(join(corpus_dir, tag_filename))
	df_pref = pd.read_table(join(corpus_dir, pref_filename))

	if graph_type == 'w':
		if pref_type == 'dense':
			print("building the dense preference graph")
			G = TriGraph(df_tag, df_pref, ifDense=True)
		else:
			print("building the sparse preference graph")
			G = TriGraph(df_tag, df_pref, ifDense=False)

	elif graph_type == 'w/o':
		print("building the graph w/o preference part")
		G = TriGraphWoPref(df_tag, df_pref)
	else:
		print("graph_type error (input should be w or w/o)")
		print("right now graph_type is :", graph_type)

	G.buildNodeList()

	G.buildMapping(graph_name+'_table')
	

	# dump table.csv
	# print("dumping the table.csv")
	# df_table.to_csv(join(corpus_dir, graph_name+'_table.csv'), index = False);

	# dump typeMap.txt
	print("dumping the typeMap.txt")
	with open(join(corpus_dir, graph_name+'_typeMap.txt'),'w') as fout:
		for key in G.dict:
			fout.write(key + ' ' + key[:4] + '\n')

	return G


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--prefFileName', type=str, default='toy_preference.txt',
                       help='preference file name')
	parser.add_argument('--tagFileName', type=str, default='toy_tags.txt',
					   help='tags file name')
	parser.add_argument('--corpus_dir', type=str, default='./corpus',
                       help='Data directory')
	parser.add_argument('--graph_name', type=str, default='graph',
                       help='graph_name')
	parser.add_argument('--graph_type', type=str, default='w',
                       help='graph_type')
	parser.add_argument('--pref_type', type=str, default='dense',
                       help='pref_type')


	args = parser.parse_args()

	G = buildGraph(args.corpus_dir, args.prefFileName, args.tagFileName, args.graph_name, args.graph_type, args.pref_type)

	writeGraph(G, args.graph_name, args.graph_type)

	

if __name__ == '__main__':
	main()
	print("--- %s seconds ---" % (time.time() - start_time))