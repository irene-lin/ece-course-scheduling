# area_cov_degree_rank.py
# Irene Lin iwl@andrew.cmu.edu
# Builds a network with students as nodes and an edge is drawn between two
# students if they took the same area or coverage course. Only students who have
# taken 4 or more area and coverage courses are included in this graph. Draws a
# degree rank plot of students with rank on the x axis and degree on the y axis.
# Draws a degree rank plot of students with rank on the x axis and degree on the
# y axis and highlights students who took their core classes in a unique order.

import networkx as nx
import ece_curriculum_library as lib
import matplotlib.pyplot as plt

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

# get 2D array of student data
data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

# build mapping of student id to core class ordering
# returns dict
def getDictionaryCoreClassOrdering(data_arr):
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

# nodes are students, edge is drawn between two students
# if they took their core classes in the same order
# returns nx.Graph
def buildCoreOrderingGraph(data_arr, d):
    G = nx.Graph()
    for i in range(1,5057+1):
        if str(i) in d and len(d[str(i)]) >= 4: G.add_node(str(i))
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

# returns a list of student ids for students with degree < 1
# on the core class ordering degree rank plot
def getIdListForUniqueCoreOrdering(data_arr):
    d = getDictionaryCoreClassOrdering(data_arr)
    G = buildCoreOrderingGraph(data_arr, d)
    arr = []
    for i in range(1,5057+1):
        if (str(i) in G and G.degree(str(i)) < 1): arr.append(i)
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=False)
    return arr

# build dictionary of student id to set of courses
# returns dict
def getDictionaryAreaCoverage(data_arr):
    d = dict()
    id = '1'
    a = []
    for line in data_arr:
        if (line[COURSE] in lib.AREA_COV):
            if line[STUDENT_ID] == id:
                a.append(line[COURSE])
            else:
                if(len(a) >= 4): d[id] = set(a)
                id = line[STUDENT_ID]
                a = [ line[COURSE]]
    if(len(a) >= 4): d[id] = set(a)
    return d

# nodes are students, edge is drawn between two students
# if they took the same area or coverage course
# returns nx.Graph
def buildAreaCoverageGraph(data_arr, d):
    G = nx.Graph()
    for i in range(1,5057+1):
        if i in d: G.add_node(i)
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            if (id1 in d and id2 in d):
                course_set1 = d[id1]
                course_set2 = d[id2]
                intersection = course_set1.intersection(course_set2)
                if (len(intersection) >= 1):
                    G.add_edge(id1, id2, weight=len(intersection))
    print(nx.info(G))
    return G

def drawDegreeRankPlot(G, id_list):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x1 = [i for i in range(len(deg_sorted))]
    y1 = [b for (a,b) in deg_sorted]
    x2 = []
    y2 = []
    for rank in range(len(deg_sorted)):
        (id, deg) = deg_sorted[rank]
        if (int(id) in id_list):
            x2.append(rank)
            y2.append(deg)
    fig, ax = plt.subplots()
    plt.scatter(x1, y1, c='black')

    if (len(id_list)>0):
        plt.scatter(x2, y2, c='yellow', label='Students with unique \ncore class ordering')
        plt.legend(loc='upper right');
    plt.title('Degree Rank Plot for Area & Coverage Courses')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.show()

d = getDictionaryAreaCoverage(data_arr)
G = buildAreaCoverageGraph(data_arr, d)
arr = getIdListForUniqueCoreOrdering(data_arr)
drawDegreeRankPlot(G, [])
drawDegreeRankPlot(G, arr)
