# ece_cores_communities.py
# Irene Lin iwl@andrew.cmu.edu

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

def getEdgelistPath(prefix, suffix):
    return 'networks/%s/cores_community_%s.edgelist' % (prefix, suffix)

def getCSVPath(prefix, suffix):
    return 'networks/%s/cores_community_%s.csv' % (prefix, suffix)

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

def getDoublesDict(d):
    dd = dict()
    for key in d:
        schedule = list(d[key])
        s = set()
        for i in range(len(schedule)):
            for j in range(i+1,len(schedule)):
                course1 = schedule[i]
                course2 = schedule[j]
                if (course1[6:] == course2[6:]):
                    s.add("%s_%s_%s" % (min(course1[2:5], course2[2:5]), max(course1[2:5], course2[2:5]), course1[6:]))
        dd[key] = s
    return dd

def countDoubles():
    d = getDictionary(data_arr)
    dd = getDoublesDict(d)
    double_counts = dict()
    for student in dd:
        for double in dd[student]:
            if (double in double_counts):
                double_counts[double] += 1
            else:
                double_counts[double] = 1
    print(double_counts)

#for all students in dictionary, draw weighted edges to every other student that took a similar course
def buildGraph(data_arr):
    G = nx.Graph()
    d = getDictionary(data_arr)
    for i in range(1,5057+1):
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            if (id1 in d and id2 in d):
                course_set1 = d[id1]
                course_set2 = d[id2]
                intersection = course_set1.intersection(course_set2)
                count = 0
                for c in intersection:
                    if (c[:5] in lib.CORE): count+=1
                if count==4: G.add_edge(id1, id2)
    print(nx.info(G))
    return G

def buildGraphWithIdList(data_arr, id_list):
    G = nx.Graph()
    d = getDictionary(data_arr)
    for i in range(len(id_list)):
        for j in range(i+1, len(id_list)):
            (id1, id2) = (str(id_list[i]), str(id_list[j]))
            course_set1 = d[id1]
            course_set2 = d[id2]
            intersection = course_set1.intersection(course_set2)
            count = 0
            for c in intersection:
                if (c[:5] in lib.CORE): count+=1
            if count==1: G.add_edge(id1, id2)
    print(nx.info(G))
    return G

def writeCoreNetwork(data_arr, suffix, id_list=None):
    if id_list==None: G = buildGraph(data_arr)
    else: G = buildGraphWithIdList(data_arr, id_list)
    lib.writeGraph(G, getEdgelistPath(cores.FILEPATH_CORE, suffix))
    lib.edgelistToCSV(getEdgelistPath(cores.FILEPATH_CORE, suffix), getCSVPath(cores.FILEPATH_CORE, suffix))


#draw network
def drawCoreNetwork(suffix):
    G = lib.readGraph(getEdgelistPath(cores.FILEPATH_CORE, suffix))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.show()

# writeCoreNetwork(data_arr, 'all', id_list)
# G = lib.readGraph(getEdgelistPath(cores.FILEPATH_CORE, 'all'))
# drawCoreNetwork('all')
# deg = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
# a = []
# for (id,degree) in deg:
#     if d[id] not in a and degree==1:
#         a.append(d[id])
#         print(id, d[id])
