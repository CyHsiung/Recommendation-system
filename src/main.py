from BuildGraph import*
import pandas as pd

if __name__ == "__main__":
    tag_filename = 'toy_tags.txt'
    pref_filename = 'toy_preference.txt'
    df_tag = readData(tag_filename)
    df_pref = readData(pref_filename)

    G = TriGraph(df_tag, df_pref)
    
    userNumber = G.userCount
    prefNumber = G.prefCount
    productDNumber = G.prodDCount
    productUNumber = G.prodUCount
    tagDNumber = G.tagDCount
    tagUNumber = G.tagUCount

    # G.buildNodeList() -> remove user without neighbors
    # G.buildNodeList(False) -> do not remove user without neighbors 
    NodeList = G.buildNodeList()
    
    '''
    for i in range(9):
        print(G.dict['user_'+str(i)])
    #print(G.NodeList)
    
    f = open('typeMap.txt','w')
    for key in G.dict:
        f.write(key + ' ' + key[:4] + '\n')

    df = G.buildMapping()
    df.to_csv('test.csv', index = False)
    '''
    