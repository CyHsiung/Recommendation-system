USERNUM=100
EPOCH=7
WINDOW=5
NEGSAMPLE=5
all: toy_extractor build_graph HIN

preprocessing:
	python ./src/preprocessing.py

toy_extractor:
	python ./src/toy_extracter.py --user_num $(USERNUM) --product_range 30-50 --output_header user$(USERNUM)

build_graph:
	python ./src/GraphBuilder.py --graph_name graph$(USERNUM) --graph_type w --pref_type sparse --prefFileName user$(USERNUM)_preference.txt --tagFileName user$(USERNUM)_tags.txt
	
semi:
	python ./src/main.py --feature_type meta2vec --graph_name graph$(USERNUM) --epochs $(EPOCH) --window $(WINDOW) --stepInEachPath 5 --negative-samples $(NEGSAMPLE) --graph_type w --log semi_E$(EPOCH)_W$(WINDOW)_NS$(NEGSAMPLE) --trainOrTest train --prefFileName user$(USERNUM)_preference.txt --tagFileName user$(USERNUM)_tags.txt &> log_semi_$(USERNUM).txt &

HIN:
	python ./src/main.py --feature_type HIN --graph_name graph$(USERNUM) --epochs $(EPOCH) --window $(WINDOW) --stepInEachPath $(WINDOW) --negative-samples $(NEGSAMPLE) --graph_type w --log HIN_E$(EPOCH)_W$(WINDOW)_NS$(NEGSAMPLE) --trainOrTest test --prefFileName user$(USERNUM)_preference.txt --tagFileName user$(USERNUM)_tags.txt
	# python ./src/main.py --feature_type HIN --graph_name graph$(USERNUM) --epochs $(EPOCH) --window $(WINDOW) --stepInEachPath $(WINDOW) --negative-samples $(NEGSAMPLE) --graph_type w --log HIN_E$(EPOCH)_W$(WINDOW)_NS$(NEGSAMPLE) --trainOrTest test --prefFileName user$(USERNUM)_preference.txt --tagFileName user$(USERNUM)_tags.txt &> log_HIN_$(USERNUM).txt &


PPR:
	# python ./src/main.py --feature_type PPR --graph_name graph --maxIter 60 --tol 1e-3 --graph_type w
	-mkdir ./PPR_log
	chmod +777 ./src/PPR_evaluate.sh
	./src/PPR_evaluate.sh
# clean:

