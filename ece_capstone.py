# ece_capstone.py
# Irene Lin iwl@andrew.cmu.edu

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib

GRADE_arr = ["1", "2", "3", "4"]
#indices
STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

CAPSTONE = {"18500", "18510", "18513", "18525", "18540",
            "18545", "18549", "18551", "18578", "18587"}

SEMESTER_arr = ["F14", "S15", "F15", "S16", "F16", "S17", "F17", "S18", "F18", "S19"]


data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

def getEdgelistPath(sem):
    return 'networks/capstone/edgelist/%s_capstone_weighted.edgelist' % sem

# return list of id numbers for students who took capstone during specific semester
# data_arr all data
# semester string from SEMESTER_arr
def getIdListByCapstoneSemester(data_arr, semester):
    id_arr = []
    for row in data_arr:
        if (row[COURSE] in CAPSTONE and row[SEMESTER] in semester):
             id_arr.append(row[STUDENT_ID])
    return id_arr

# data_arr all data
# semester string from SEMESTER_arr
def getCapstoneDataArr(data_arr, semester):
    id_arr = getIdListByCapstoneSemester(data_arr, semester)
    capstone_data_arr = lib.partitionDataById(id_arr, data_arr)
    return capstone_data_arr

def buildCapstoneNetwork(data_arr, semester):
    capstone_data_arr = getCapstoneDataArr(data_arr, semester)
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in capstone_data_arr:
        if (row[STUDENT_ID] == id and row[COURSE] in lib.AREA.union(lib.COVERAGE)):
            #same student, add course to array
            courses_arr.append(row[1])
        else:
            #diff student
            G = lib.addWeightedEdges(G,courses_arr)
            #update id, clear arr
            id = row[0]
            courses_arr = []
    # print(nx.info(G))
    return G

def printMetrics(G, data_arr, sem):
    if (len(nx.edges(G))>0):
        c = nx.average_clustering(G, nodes=None, weight='weight')
        degree = 0
        for n in nx.degree(G):
            degree+=n[1]
            weighted_degree =0
            degree = degree / len(nx.nodes(G))
        for n in nx.degree(G, None, 'weight'):
            weighted_degree+=n[1]
            weighted_degree = weighted_degree / len(nx.nodes(G))
    else:
        c = 0
        degree = 0
        weighted_degree = 0
    print('capstone %s\t'               %sem,
          'nodes: %d\t'                 % len(nx.nodes(G)),
          'edges: %d\t '                % len(nx.edges(G)),
          'avg degree: %f\t'            % degree,
          'avgweighted degree: %f\t'    % weighted_degree,
          'avg weighted clustering %f\t'% c,
          'weighted triangles: %d\t'    % sum((nx.triangles(G)).values()),
          'num students: %d'            % len(getIdListByCapstoneSemester(data_arr, sem))
          )

def writeCapstoneNetwork(data_arr, sem):
    G = buildCapstoneNetwork(data_arr, sem)
    lib.writeGraph(G, getEdgelistPath(sem))
    printMetrics(G, data_arr, sem)
    #lib.edgelistToCSV(getEdgelistPath(sem), 'networks/capstone/csv/%s_capstone_weighted.csv' % sem)


def drawCapstoneNetwork(sem):
    G = lib.readGraph(getEdgelistPath(sem))
    pos=nx.spring_layout(G,scale=10)
    for e in nx.edges(G):
        nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.1)
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.DEVICES),node_size=400, node_color='#66ffff', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.CIRCUITS),node_size=400, node_color='#99ff66', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.HARDWARE),node_size=400, node_color='#ffff00', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.SOFTWARE),node_size=400, node_color='#ff9999', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.SIGNALS),node_size=400, node_color='#9999ff', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    # plt.title(' '.join([course, sem, grade]))
    plt.show()


# drawCapstoneNetwork()
for sem in SEMESTER_arr:
    writeCapstoneNetwork(data_arr, sem)
