import numpy as np
import json
from os.path import join
import sys
sys.path.append("../")

from BuildGraph import*

#node embeddings of "yi"
# print(node_embeddings[nodeid2index["product_D_35"]])
project_dir = '../../'
corpus_dir = join(project_dir, 'corpus')

def output_numpy(userNum, prodNum, embedDim):
    # read dictionary form json file
    index2nodeid = json.load(open("./log/index2nodeid.json"))
    index2nodeid = {int(k):v for k,v in index2nodeid.items()}
    nodeid2index = {v:int(k) for k,v in index2nodeid.items()}
    node_embeddings = np.load("./log/node_embeddings.npz")['arr_0']

    # start
    userEmbed = np.zeros((userNum, embedDim))
    missingUser = []
    for i in range(userNum):
        if 'user_' + str(i) not in nodeid2index:
            missingUser.append('user_' + str(i))
        else:
            userEmbed[i, :] = node_embeddings[nodeid2index['user_' + str(i)]]
    prodEmbed = np.zeros((prodNum, embedDim * 2))
    for i in range(prodNum):
        if 'product_D_' + str(i) in nodeid2index:
            prodEmbed[i, 0 : embedDim] = node_embeddings[nodeid2index['product_D_' + str(i)]]
        if 'product_U_' + str(i) in nodeid2index:
            prodEmbed[i, embedDim : 2 * embedDim] = node_embeddings[nodeid2index['product_U_' + str(i)]]
    return userEmbed, prodEmbed, missingUser
        
    

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

if __name__ == '__main__':
    embedDim = 100
    tag_filename = join(project_dir, 'corpus/toy_tags.txt')
    pref_filename = join(project_dir, 'corpus/toy_preference.txt')
    nodeById, userNum, prodNum = import_graph(tag_filename, pref_filename)
    userEmbed, prodEmbed, missingUser = output_numpy(userNum, prodNum, embedDim)
    print(userEmbed.shape)
    print(prodEmbed.shape)
    print(missingUser)
    
