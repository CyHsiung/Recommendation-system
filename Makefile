SHELL=/bin/bash
all: preprocessing toy_extractor semi

preprocessing:
	python ./src/preprocessing.py

toy_extractor:
	python ./src/toy_extracter.py --user_num 10 --product_range 3-5

build_graph:
	python ./src/GraphBuilder.py
	
semi:
	python ./src/main.py --feature_type meta2vec

# clean:

