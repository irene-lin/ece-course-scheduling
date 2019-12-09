# ece_area_communities.py
# Irene Lin iwl@andrew.cmu.edu
# Builds a network or students and draws an edge between two students if they
# have n or more area/coverage courses in common where n is a parameter for
# similarity threshold.

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

FILEPATH_AREA = 'area_coverage'
COMMON_AREA = ["18349", "18330", "18341", "18794", "18491", "18370", "18447", "15440"]

#get data_set
data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

def getEdgelistPath(prefix, suffix):
    return 'networks/%s/area_community_%s.edgelist' % (prefix, suffix)

def getCSVPath(prefix, suffix):
    return 'networks/%s/area_community_%s.csv' % (prefix, suffix)

#build dictionary of student id to set of courses
def getDictionary(data_arr):
    counts = dict()
    d = dict()
    id = '1'
    a = []
    for line in data_arr:
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
    # print(counts)
    return d

#for all students in dictionary, draw weighted edges to
#every other student that took the same course
def buildGraph(data_arr, sim_thresh):
    G = nx.Graph()
    d = getDictionary(data_arr)
    for i in range(1,5057+1):
        if i in d: G.add_node(i)
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

def writeAreaNetwork(data_arr, sim_thresh):
    G = buildGraph(data_arr, sim_thresh)
    lib.writeGraph(G, getEdgelistPath(FILEPATH_AREA, str(sim_thresh)))
    lib.edgelistToCSV(getEdgelistPath(FILEPATH_AREA, str(sim_thresh)),
                                            getCSVPath(FILEPATH_AREA, str(sim_thresh)))

def drawNetwork(data_arr, sim_thresh):
    G = lib.readGraph(getEdgelistPath(FILEPATH_AREA, str(sim_thresh)))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=5)
    plt.axis('off')
    plt.show()

# plot rank vs degree
def degreeRankPlot(G):
    sorted_by_second = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    rank_freq = [x[1] for x in sorted_by_second]
    _ = plt.plot(rank_freq)
    plt.title("degree rank")
    plt.show()

def getDegreeRankArr(G):
    sorted_by_second = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    return sorted_by_second

def printAreaCovRankConditionedByIdList(sim_thresh, data_arr, infile):
    d = getDictionary(data_arr)
    G = lib.readGraph(getEdgelistPath(FILEPATH_AREA, str(sim_thresh)))
    sorted_by_second = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    f_in = open(infile, "r")
    arr = f_in.read().split()
    for i in range(len(sorted_by_second)):
        id,deg = sorted_by_second[i]
        if id in arr: print(i+1,",", id,",",deg)

drawNetwork(data_arr, 5)
writeAreaNetwork(data_arr, 5)
