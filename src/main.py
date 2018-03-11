from BuildGraph import*
import pandas as pd

if __name__ == "__main__":
    tag_filename = 'toy_tags.txt'
    pref_filename = 'toy_preference.txt'
    df_tag = readData(tag_filename)
    df_pref = readData(pref_filename)

    G = TriGraph()
    G.buildGraghFromProduct(df_tag)
    G.buildGraghFromUser(df_pref)

    userNumber = G.userCount
    prefNumber = G.prefCount
    productDNumber = G.prodDCount
    productUNumber = G.prodUCount
    tagDNumber = G.tagDCount
    tagUNumber = G.tagUCount
    G.buildNodeList()
    print(G.NodeList)
    
    #df = G.buildMapping()
    #df.to_csv('test.csv',index = False)