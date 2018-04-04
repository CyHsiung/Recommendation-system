all: toy_extractor build_graph PPR

preprocessing:
	python ./src/preprocessing.py

toy_extractor:
	python ./src/toy_extracter.py --user_num 10 --product_range 30-50

build_graph:
	python ./src/GraphBuilder.py --graph_name graph --graph_type w/o
	
semi:
	python ./src/main.py --feature_type meta2vec --graph_name graph --epochs 1 --window 5 --negative-samples 10 --graph_type w/o

PPR:
	python ./src/main.py --feature_type PPR --graph_name graph --maxIter 60 --tol 1e-3 --graph_type w/o
	# -mkdir ./PPR_log
	# chmod +777 ./src/PPR_evaluate.sh
	# ./src/PPR_evaluate.sh
# clean:

