all: toy_extractor build_graph semi

preprocessing:
	python ./src/preprocessing.py

toy_extractor:
	python ./src/toy_extracter.py --user_num 10 --product_range 30-50

build_graph:
	python ./src/GraphBuilder.py --graph_name graph
	
semi:
	python ./src/main.py --feature_type meta2vec --graph_name graph --epochs 1 --window 3 --negative-samples 7

PPR:
	python ./src/main.py --feature_type PPR --graph_name graph 
# clean:

