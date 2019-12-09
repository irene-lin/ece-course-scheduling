# ece_capstone.py
# Irene Lin iwl@andrew.cmu.edu
# Builds a network of students who took capstone in the same academic year and
# draws an edge between two nodes if two students took the same area or coverage
# course.

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

def getEdgelistPath(semester_fall, semester_spring, sim_thresh):
    return 'networks/capstone/edgelist/%s_%s_capstone_%d.edgelist' % (semester_fall, semester_spring, sim_thresh)

def getCSVPath(semester_fall, semester_spring, sim_thresh):
    return 'networks/capstone/edgelist/%s_%s_capstone_%d.csv' % (semester_fall, semester_spring, sim_thresh)

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

#build dictionary of student id to set of courses
def getDictionary(data_arr, semester_fall, semester_spring):
    capstone_data_arr = getCapstoneDataArr(data_arr, semester_fall, semester_spring)
    counts = dict()
    d = dict()
    id = capstone_data_arr[1][STUDENT_ID]
    a = []
    for line in capstone_data_arr:
        if (line[COURSE] in lib.AREA_COV):
            if line[STUDENT_ID] == id:
                a.append(line[COURSE])
            else:
                d[id] = set(a)
                id = line[STUDENT_ID]
                a = [ line[COURSE]]
            if (line[COURSE] in counts):
                counts[line[COURSE]] += 1
            else:
                counts[line[COURSE]] = 1
    d[id] = set(a)
    print(len(d))
    a = []
    for c in counts:
        a.append((c, counts[c]))
    print(sorted(a, key=lambda tup: tup[1], reverse=True))
    return d

#courses as nodes
def buildGraphCourses(data_arr, semester_fall, semester_spring):
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

#students as nodes
def buildGraphStudents(data_arr, semester_fall, semester_spring, sim_thresh):
    d = getDictionary(data_arr, semester_fall, semester_spring)
    G = nx.Graph()
    for i in range(1,5057+1):
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            if (id1 in d and id2 in d):
                course_set1 = d[id1]
                course_set2 = d[id2]
                intersection = course_set1.intersection(course_set2)
                if (len(intersection) >= sim_thresh):
                    G.add_edge(id1, id2, weight=len(intersection))
    print(nx.info(G))
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

def writeCapstoneNetwork(data_arr, semester_fall, semester_spring, sim_thresh):
    if (sim_thresh == 0):
        G = buildGraphCourses(data_arr, semester_fall, semester_spring)
        printMetrics(G, data_arr, semester_fall, semester_spring, sim_thresh)
    else:
        G = buildGraphStudents(data_arr, semester_fall, semester_spring, sim_thresh)
    lib.writeGraph(G, getEdgelistPath(semester_fall, semester_spring, sim_thresh))
    lib.edgelistToCSV(getEdgelistPath(semester_fall, semester_spring, sim_thresh),
                      getCSVPath(semester_fall, semester_spring, sim_thresh))


def drawCapstoneNetwork(semester_fall, semester_spring, sim_thresh):
    G = lib.readGraph(getEdgelistPath(semester_fall, semester_spring, sim_thresh))
    pos=nx.spring_layout(G,scale=10)

    if (sim_thresh == 0):
        for e in nx.edges(G):
            nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.1)
        nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
        nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.DEVICES),node_size=400, node_color='#66ffff', node_shape='o')
        nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.CIRCUITS),node_size=400, node_color='#99ff66', node_shape='o')
        nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.HARDWARE),node_size=400, node_color='#ffff00', node_shape='o')
        nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.SOFTWARE),node_size=400, node_color='#ff9999', node_shape='o')
        nx.draw_networkx_nodes(G,pos,nodelist=lib.getNodeinSet(G,lib.SIGNALS),node_size=400, node_color='#9999ff', node_shape='o')
    else:
        nx.draw_networkx_edges(G,pos,edge_color='b')
        nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.title('Capstone %s %s SIM_THRESH %d' %(semester_fall, semester_spring, sim_thresh))
    plt.show()

(semester_fall, semester_spring, sim_thresh) = ('F18', 'S19', 4)
writeCapstoneNetwork(data_arr, semester_fall, semester_spring, sim_thresh)
drawCapstoneNetwork(semester_fall, semester_spring, sim_thresh)
