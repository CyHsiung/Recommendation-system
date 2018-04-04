import json
from src.graphProcessing.BuildGraph import*
from src.graphProcessing.BuildGraphWoPref import*

def writeGraph(graph, outfileName, graphType):
    outJsonfileName = './corpus/' + outfileName + '.json'
    outCountfileName = './corpus/' + outfileName + '.count'
    print("Writing NodeList into", outJsonfileName)
    with open(outJsonfileName, 'w') as outfile:
        json.dump(graph.NodeList, outfile)

    print("Writing numbers of nodes into", outCountfileName)
    with open(outCountfileName, 'w') as outfile:
        outfile.write(str(graph.userNum))
        outfile.write('\n')
        outfile.write(str(graph.userCount))
        outfile.write('\n')
        if graphType == "w":
            outfile.write(str(graph.prefCount))
        else: outfile.write('0')
        outfile.write('\n')
        outfile.write(str(graph.prodUCount))
        outfile.write('\n')
        outfile.write(str(graph.prodDCount))
        outfile.write('\n')
        outfile.write(str(graph.tagUCount))
        outfile.write('\n')
        outfile.write(str(graph.tagDCount))
    print('Writing Done')
        
def readGraph(fileName, graphType):
    jsonfileName = './corpus/' + fileName + '.json'
    countfileName = './corpus/' + fileName + '.count' 
    print('Reading NodeList from', jsonfileName)
    with open(jsonfileName, 'r') as json_data:
        d = json.load(json_data)
    
    print('Reading numbers of nodes from', countfileName)
    l = []
    f = open(countfileName, 'r')
    line = f.readline()
    while line:
        line=line.strip().split()
        l.append(int(line[0]))
        line = f.readline()
    if graphType == 'w':
        graph = TriGraph(userNum=l[0], userCount=l[1], 
                    prefCount=l[2], prodUCount=l[3], prodDCount=l[4], tagUCount=l[5], tagDCount=l[6], NodeList=d)
    else:
        graph = TriGraphWoPref(userNum=l[0], userCount=l[1], 
                    prodUCount=l[3], prodDCount=l[4], tagUCount=l[5], tagDCount=l[6], NodeList=d)
    print('Reading Done')
    return graph