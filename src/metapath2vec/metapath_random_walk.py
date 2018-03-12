import numpy as np
from os.path import join
import random

import sys
sys.path.append("../")

from BuildGraph import*
import pandas as pd

project_dir = '../../'
corpus_dir = join(project_dir, 'corpus')

def import_graph(tag_filename, pref_filename):
    df_tag = readData(tag_filename)
    df_pref = readData(pref_filename)

    G = TriGraph(df_tag, df_pref)
    # G.buildNodeList() -> remove user without neighbors
    # G.buildNodeList(False) -> do not remove user without neighbors 
    G.buildNodeList()
    userNum = G.userCount
    prodNum = G.prodDCount
    return G.NodeList, userNum, prodNum
    


def create_path(num, catagory, stepInEachPath, f, nodeById, meta_path_format): 
    
    for i in range(num):
        startKey = catagory + '_' + str(i)
        if startKey not in nodeById:
            continue
        # curNode is a dictionary with:
        # Id, Type, next_user, next_pref, next_prod, next_tags
        curNode = nodeById[startKey]
        # type of start node index in meta_path_format
        # so the next one's type would be idBias + 1 
        idBias = meta_path_format.index(curNode['Type'])
        f.write("{}".format(curNode['Id']))
        for j in range(stepInEachPath - 1):
            nextTypeId = (j + idBias + 1) % len(meta_path_format)
            nextType = meta_path_format[nextTypeId]
            if curNode['next_' + nextType]: 
                nextId = random.choice(curNode['next_' + nextType])
                if nextId == curNode['Id'] and len(curNode['next_' + nextType]) == 1:
                    break
                while nextId == curNode['Id']:
                    nextId = random.choice(curNode["next_" + nextType])
            else:
                candidate = []
                for k in curNode:
                    if isinstance(curNode[k], list) and k != 'next_' + curNode['Type']:
                        
                        for x in curNode[k]:
                            candidate.append(x)
                if not candidate:
                    print(nextType, curNode['Type'], '\n', curNode)
                    break
                nextId = random.choice(candidate)
            curNode = nodeById[nextId]
            f.write(" {}".format(curNode['Id']))
        f.write("\n")
def metaPath_random_walk(userNum, prodNum, stepInEachPath, writeFileName, nodeById, meta_path_format):
    f = open(join(corpus_dir, writeFileName), 'w')
    create_path(userNum, 'user', stepInEachPath, f, nodeById, meta_path_format)
    create_path(prodNum, 'product_U', stepInEachPath, f, nodeById, meta_path_format)
    create_path(prodNum, 'product_D', stepInEachPath, f, nodeById, meta_path_format)
    f.close()
                
if __name__ == '__main__':
    stepInEachPath = 20
    writeFileName = 'random_walk.txt'
    meta_path_format = ['user', 'pref', 'prod', 'tags', 'prod', 'pref']
    tag_filename = join(project_dir, 'corpus/toy_tags.txt')
    pref_filename = join(project_dir, 'corpus/toy_preference.txt')
    nodeById, userNum, prodNum = import_graph(tag_filename, pref_filename)
    metaPath_random_walk(userNum, prodNum, stepInEachPath, writeFileName, nodeById, meta_path_format) 
