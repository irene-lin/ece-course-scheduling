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

def getEdgelistPath(semester_fall, semester_spring):
    return 'networks/capstone/edgelist/%s_%s_capstone_weighted.edgelist' % (semester_fall, semester_spring)

# return list of id numbers for students who took capstone during specific semester
# data_arr all data
# semester string from SEMESTER_arr
def getIdListByCapstoneSemester(data_arr, semester_fall, semester_spring):
    id_arr = []
    for row in data_arr:
        if (row[COURSE] in CAPSTONE and row[SEMESTER] in (semester_fall + semester_spring)):
             id_arr.append(row[STUDENT_ID])
    return id_arr

# data_arr all data
# semester string from SEMESTER_arr
def getCapstoneDataArr(data_arr, semester_fall, semester_spring):
    id_arr = getIdListByCapstoneSemester(data_arr, semester_fall, semester_spring)
    capstone_data_arr = lib.partitionDataById(id_arr, data_arr)
    return capstone_data_arr

def buildCapstoneNetwork(data_arr, semester_fall, semester_spring):
    capstone_data_arr = getCapstoneDataArr(data_arr, semester_fall, semester_spring)
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

def printMetrics(G, data_arr, semester_fall, semester_spring):
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
    print('capstone %s %s\t'               % (semester_fall, semester_spring),
          'nodes: %d\t'                 % len(nx.nodes(G)),
          'edges: %d\t '                % len(nx.edges(G)),
          'avg degree: %f\t'            % degree,
          'avgweighted degree: %f\t'    % weighted_degree,
          'avg weighted clustering %f\t'% c,
          'weighted triangles: %d\t'    % sum((nx.triangles(G)).values()),
          'num students: %d'            % len(getIdListByCapstoneSemester(data_arr, semester_fall, semester_spring))
          )

def writeCapstoneNetwork(data_arr, semester_fall, semester_spring):
    G = buildCapstoneNetwork(data_arr, semester_fall, semester_spring)
    lib.writeGraph(G, getEdgelistPath(semester_fall, semester_spring))
    printMetrics(G, data_arr, semester_fall, semester_spring)
    lib.edgelistToCSV(getEdgelistPath(semester_fall, semester_spring),
                     'networks/capstone/csv/%s_%s_capstone_weighted.csv'
                     % (semester_fall, semester_spring))


def drawCapstoneNetwork(semester_fall, semester_spring):
    G = lib.readGraph(getEdgelistPath(semester_fall, semester_spring))
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
    plt.title('Capstone %s %s' %(semester_fall, semester_spring))
    plt.show()


# drawCapstoneNetwork()
# SEMESTER_arr.reverse()
for i in range(0, len(SEMESTER_arr), 2):
    # writeCapstoneNetwork(data_arr, SEMESTER_arr[i], SEMESTER_arr[i+1])
    drawCapstoneNetwork(SEMESTER_arr[i], SEMESTER_arr[i+1])
