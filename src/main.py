from BuildGraph import*
import pandas as pd

if __name__ == "__main__":
    tag_filename = '../corpus/toy_tags.txt'
    pref_filename = '../corpus/toy_preference.txt'
    df_tag = readData(tag_filename)
    df_pref = readData(pref_filename)
    G = TriGraph(df_tag, df_pref)
    
    # G.buildNodeList() -> remove user without neighbors
    # G.buildNodeList(False) -> do not remove user without neighbors 
    G.buildNodeList()
    NodeList = G.NodeList
    
    #counts: [userNum, prefNum, prodUNum, prodDNum, tagUNum, tagDNum]
    #G.getCount(False) -> user without neighbor still counts
    #G.getCount() -> user without neighbor does not count
    counts = G.getCount(False)
    print(counts)
    
    '''
    for i in range(9):
        print(G.dict['user_'+str(i)])
    #print(G.NodeList)
    
    f = open('../corpus/typeMap.txt','w')
    for key in G.dict:
        f.write(key + ' ' + key[:4] + '\n')
    df = G.buildMapping()
    df.to_csv('../corpus/test.csv', index = False)
    '''
