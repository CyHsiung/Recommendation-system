from os.path import join
import os
import sys

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
def meta2vec(nodeById = None, userNum = None, prodNum = None, tag_fileName = None, pref_fileName = None, args = None): 
    stepInEachPath = args.stepInEachPath
    embedDim = 100
    writeFileName = 'random_walk.txt'
    meta_path_format = ['user', 'pref', 'prod', 'tags', 'prod', 'pref']
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
    main(args)
    # output two embed matrix and the miss user list
    userEmbed, prodEmbed, missingUser = output_numpy(userNum, prodNum, embedDim)
    return userEmbed, prodEmbed, missingUser

if __name__ == '__main__':
    userEmbed, prodEmbed, missingUser = meta2vec()
    print(userEmbed.shape)
    print(prodEmbed.shape)
    print(missingUser)
    
    
