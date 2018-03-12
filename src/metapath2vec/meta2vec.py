from metapath_random_walk import import_graph, metaPath_random_walk
from train import main, parse_args
from extract import output_numpy
from os.path import join
import os

# project_dir: Recommedation/
project_dir = os.path.abspath('./')
while project_dir[-3:] != 'src':
    project_dir = os.path.abspath(join(project_dir, os.pardir))
project_dir = join(project_dir, '..')
corpus_dir = join(project_dir, 'corpus')
def meta2vec(): 
    stepInEachPath = 20
    embedDim = 100
    writeFileName = 'random_walk.txt'
    meta_path_format = ['user', 'pref', 'prod', 'tags', 'prod', 'pref']
    tag_filename = join(project_dir, 'corpus/toy_tags.txt')
    pref_filename = join(project_dir, 'corpus/toy_preference.txt')
    # get graph parameter
    nodeById, userNum, prodNum = import_graph(tag_filename, pref_filename)
    # produce random path
    metaPath_random_walk(userNum, prodNum, stepInEachPath, writeFileName, nodeById, meta_path_format)
    # train the model 
    args = parse_args(embedDim)
    main(args)
    # output two embed matrix and the miss user list
    userEmbed, prodEmbed, missingUser = output_numpy(userNum, prodNum, embedDim)
    return userEmbed, prodEmbed, missingUser

if __name__ == '__main__':
    userEmbed, prodEmbed, missingUser = meta2vec()
    print(userEmbed.shape)
    print(prodEmbed.shape)
    print(missingUser)
    
    
