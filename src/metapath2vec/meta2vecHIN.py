from os.path import join
import os
import sys
from os.path import join

# project_dir: Recommedation/
project_dir = os.path.abspath('./')
'''
while project_dir[-3:] != 'src':
    project_dir = os.path.abspath(join(project_dir, os.pardir))
project_dir = join(project_dir, '..')
'''
sys.path.append(project_dir)

from src.metapath2vec.metapath_random_walk import import_graph, metaPath_random_walk
from src.metapath2vec.train import main, parse_args
from src.metapath2vec.extract import output_numpy

corpus_dir = join(project_dir, 'corpus')
models_dir = join(project_dir, 'models')
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

def meta2vec_for_HIN(meta_path_format, number, nodeById = None, userNum = None, prodNum = None, tag_fileName = None, pref_fileName = None, args = None): 
    stepInEachPath = args.stepInEachPath
    embedDim = 100
    writeFileName = 'random_walk.txt'
        
    if not tag_fileName:
        tag_fileName = join(project_dir, 'corpus/toy_tags.txt')
    if not pref_fileName:
        pref_fileName = join(project_dir, 'corpus/toy_preference.txt')
    # get graph parameter
    if not nodeById:
        nodeById, userNum, prodNum = import_graph(tag_fileName, pref_fileName)
    # produce random path
    metaPath_random_walk(userNum, prodNum, stepInEachPath, writeFileName, nodeById, meta_path_format)
    # train the model 
    # args = parse_args(embedDim, nEpoch, windowSize)
    # args.log = join(models_dir, "metaHIN_" + str(number))
    print(args.log)
    main(args)
    # output two embed matrix and the miss user list
    userEmbed, prodEmbed, missingUser = output_numpy(userNum, prodNum, embedDim, args.log)
    return userEmbed, prodEmbed, missingUser

def meta2vecHIN(args, nodeById, userNum, prodNum, tag_fileName = None, pref_fileName = None, metaPathList = None):
    if metaPathList == None:
        metaPathList = [['prod', 'tags'], ['user', 'pref', 'prod', 'tags', 'prod', 'pref']]
    userEmbedList = []
    prodEmbedList = []
    for i in range(len(metaPathList)):
        user_feature, item_feature, _ = meta2vec_for_HIN(nodeById = nodeById, userNum = userNum, prodNum = prodNum, args = args, meta_path_format = metaPathList[i], number = i)
        userEmbedList.append(user_feature)
        prodEmbedList.append(item_feature)
    return userEmbedList, prodEmbedList
           


if __name__ == '__main__':
    userEmbed, prodEmbed, missingUser = meta2vec()
    print(userEmbed.shape)
    print(prodEmbed.shape)
    print(missingUser)
    
    
