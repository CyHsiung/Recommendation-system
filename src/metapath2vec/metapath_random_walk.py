import numpy as np
from os.path import join

feats_dir = '../data/'
def metaPath_random_walk(pathNum, stepInEachPath, writeFileName, nodeById, meta_path_format):
    f = open(join(feats_dir, writeFileName), 'w')
    for i in range(pathNum):
        startKey = random.choice(list(nodeById.keys()))
        curNode = nodeById[startKey]
        # type of start node index in meta_path_format
        # so the next one's type would be idBias + 1 
        idBias = meta_path_format.index(curNode[Type])
        f.write("{}".format(curNode[Id]))
        for j in range(stepInEachPath - 1):
            nextTypeId = (j + idBias) % len(nodeById)
            nextType = meta_path_format[nextTypeId]
            if curNode[nextType]: 
                nextNodeId = random.choice(curNode[nextType])
                if nextNode.Id == curNode.Id and len(curNode) == 1:
                    break
                while nextNode.Id == curNode.Id:
                    nextNodeId = random.choice(curNode[nextType])
            else:
                candidate = []
                for k in nodeById:
                    if isinstance(nodeById[k], list) and k != nextType:
                        for x in nodebyId[k]:
                            candidate.append(x)
                nextNodeId = random.choice(candidate)
                if not candidate:
                    break
            curNode = nodeById[nextNodeId]
            f.write(" {}".format(curNode[Id]))

        f.write("\n")
    f.close()
        
def generate_test_data(dataNum):
    nodeById = {}
    meta_path_format = [next_user, next_pref, next_prod, next_tags, next_prod, next_pref]
    for i in range(dataNum):
                


if __name__ == '__main__':
    pathNum = 10
    writeFileName = 'random_walk.txt'
    meta_path_format = [next_user, next_pref, next_prod, next_tags, next_prod, next_pref]
    nodeById = 
    metaPath_random_walk(pathNum, writeFileName, nodeById, meta_path_format) 
