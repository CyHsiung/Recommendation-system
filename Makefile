all: preprocessing toy_extractor semi

preprocessing:
	python ./src/preprocessing.py

toy_extractor:
	time python ./src/toy_extracter.py --user_num 50 --product_range 30-50

build_graph:
	time python ./src/GraphBuilder.py --graph_name graph
	
semi:
	python ./src/main.py --feature_type meta2vec

# clean:

