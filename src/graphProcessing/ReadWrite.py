import json
from src.graphProcessing.BuildGraph import*

def writeGraph(graph, outfileName):
    outJsonfileName = './corpus/' + outfileName + '.json'
    outCountfileName = './corpus/' + outfileName + '.count'
    with open(outJsonfileName, 'w') as outfile:
        json.dump(graph.NodeList, outfile)
    with open(outCountfileName, 'w') as outfile:
        outfile.write(str(graph.userNum))
        outfile.write('\n')
        outfile.write(str(graph.userCount))
        outfile.write('\n')
        outfile.write(str(graph.prefCount))
        outfile.write('\n')
        outfile.write(str(graph.prodUCount))
        outfile.write('\n')
        outfile.write(str(graph.prodDCount))
        outfile.write('\n')
        outfile.write(str(graph.tagUCount))
        outfile.write('\n')
        outfile.write(str(graph.tagDCount))
        
def readGraph(fileName):
    jsonfileName = './corpus/' + fileName + '.json'
    countfileName = './corpus/' + fileName + '.count' 
    with open(jsonfileName, 'r') as json_data:
        d = json.load(json_data)
    l = []
    f = open(countfileName, 'r')
    line = f.readline()
    while line:
        line=line.strip().split()
        l.append(int(line[0]))
        line = f.readline()

    graph = TriGraph(userNum=l[0], userCount=l[1], 
                prefCount=l[2], prodUCount=l[3], prodDCount=l[4], tagUCount=l[5], tagDCount=l[6], NodeList=d)
    return graph