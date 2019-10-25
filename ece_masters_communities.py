# ece_masters_communities.py
# Irene Lin iwl@andrew.cmu.edu

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib
import ece_masters as masters

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER
FILEPATH_GRAD = 'grad'

data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

def getEdgelistPath(prefix, suffix):
    return 'networks/%s/masters_community_%s.edgelist' % (prefix, suffix)

def getCSVPath(prefix, suffix):
    return 'networks/%s/masters_community_%s.csv' % (prefix, suffix)

#build dictionary of student id to set of courses
def getDictionary(data_arr):
    d = dict()
    id = '1'
    a = []
    for line in data_arr:
        if (line[GRADE] == '10' and line[COURSE][:2] != '18'):
            if line[STUDENT_ID] == id:
                a.append(line[COURSE])
            else:
                d[id] = set(a)
                id = line[STUDENT_ID]
                a = [ line[COURSE]]
    d[id] = set(a)
    return d

#for all students in dictionary, draw weighted edges to every other student that took a similar course
def buildGraph(data_arr, similarity_target):
    G = nx.Graph()
    d = getDictionary(data_arr)
    s = set()
    for i in range(1,5057+1):
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            if (id1 in d and id2 in d):
                course_set1 = d[id1]
                course_set2 = d[id2]
                intersection = course_set1.intersection(course_set2)
                count = 0
                for c in intersection:
                    if (c not in masters.CONCENTRATIONS): count+=1
                if count>=similarity_target:
                    G.add_edge(id1, id2)
                    s.add(tuple(sorted(list(intersection))))
    print(nx.info(G))
    for item in s:
        print(item)
    return G

def writeMastersNetwork(data_arr, suffix, similarity_target):
    G = buildGraph(data_arr, similarity_target)
    lib.writeGraph(G, getEdgelistPath(FILEPATH_GRAD, suffix))
    lib.edgelistToCSV(getEdgelistPath(FILEPATH_GRAD, suffix), getCSVPath(FILEPATH_GRAD, suffix))


#draw network
def drawMastersNetwork(suffix):
    G = lib.readGraph(getEdgelistPath(FILEPATH_GRAD, suffix))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.show()

def printScheduleBuckets():
    d = getDictionary(data_arr)
    G = lib.readGraph(getEdgelistPath(FILEPATH_GRAD, 'all'))
    deg = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    a = []
    for (id,degree) in deg:
        if degree not in a:
            a.append(degree)
            print(degree, d[id])

writeMastersNetwork(data_arr, 'all', 6)
drawMastersNetwork('all')
# printScheduleBuckets()
