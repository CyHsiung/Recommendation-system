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
    return G.NodeList
    

def metaPath_random_walk(pathNum, stepInEachPath, writeFileName, nodeById, meta_path_format):
    f = open(join(corpus_dir, writeFileName), 'w')
    for i in range(pathNum):
        startKey = random.choice(list(nodeById.keys()))
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
            print(curNode['Type'],', ', nextType)
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
                nextNodeId = random.choice(candidate)
            curNode = nodeById[nextId]
            f.write(" {}".format(curNode['Id']))

        f.write("\n")
    f.close()
        
                
if __name__ == '__main__':
    pathNum = 10
    stepInEachPath = 10
    writeFileName = 'random_walk.txt'
    meta_path_format = ['user', 'pref', 'prod', 'tags', 'prod', 'pref']
    tag_filename = join(project_dir, 'corpus/toy_tags.txt')
    pref_filename = join(project_dir, 'corpus/toy_preference.txt')
    nodeById = import_graph(tag_filename, pref_filename)
    metaPath_random_walk(pathNum, stepInEachPath, writeFileName, nodeById, meta_path_format) 
