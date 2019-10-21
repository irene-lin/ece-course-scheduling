# ece_cores_communities.py
# Irene Lin iwl@andrew.cmu.edu
# data_set = students who took a specific core
# partition by which semester they took the core
# map when other cores were taken
# map which other area/coverage courses were taken

#nodes are students, edges are classes taken together


import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib
import ece_cores as cores

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

#get data_set
data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

def getEdgelistPath(prefix):
    return 'networks/%s/cores_community.edgelist' % (prefix)

def getCSVPath(prefix):
    return 'networks/%s/cores_community.csv' % (prefix)

#build dictionary of student id to set of courses
def getDictionary(data_arr):
    d = dict()
    id = '1'
    a = []
    for line in data_arr:
        if (line[COURSE] in lib.CORE):
            if line[STUDENT_ID] == id:
                a.append(line[COURSE]+'_'+line[GRADE]+line[SEMESTER][0])
            else:
                d[id] = set(a)
                id = line[STUDENT_ID]
                a = [ line[COURSE]+'_'+line[GRADE]+line[SEMESTER][0] ]
    d[id] = set(a)
    return d

#add all nodes to network
def addNodes(G, id_list):
    for id in id_list:
        G.add_node(id)
    return G

def addWeightedEdge(G,id1,id2):
    #incr weight
    if ((id1,id2) in nx.edges(G)):
        new_weight = G[id1][id2]['weight'] + 1
        G.add_edge(id1, id2, weight=new_weight)
    #add to network with weight 1
    else:
        G.add_edge(id1, id2, weight=1)
    return G

#for all students in dictionary, draw weighted edges to every other student that took a similar course
def buildGraph(data_arr):
    G = nx.Graph()
    d = getDictionary(data_arr)
    for i in range(1,5057+1):
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            course_set1 = d[id1]
            course_set2 = d[id2]
            intersection = course_set1.intersection(course_set2)
            count = 0
            for c in intersection:
                if (c[:5] in lib.CORE): count+=1
            if count==4: G.add_edge(id1, id2)
    print(nx.info(G))
    return G

def writeCoreNetwork(data_arr):
    G = buildGraph(data_arr)
    lib.writeGraph(G, getEdgelistPath(cores.FILEPATH_CORE))
    lib.edgelistToCSV(getEdgelistPath(cores.FILEPATH_CORE), getCSVPath(cores.FILEPATH_CORE))


#draw network
def drawCoreNetwork():
    G = lib.readGraph(getEdgelistPath(cores.FILEPATH_CORE))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.show()

d = getDictionary(data_arr)
# a = [887, 1480]
# for id in a:
#     print(id, d[str(id)])

G = lib.readGraph(getEdgelistPath(cores.FILEPATH_CORE))
deg = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
a = []
for (id,degree) in deg:
    if d[id] not in a:
        a.append(d[id])
        print(degree, id, d[id])
