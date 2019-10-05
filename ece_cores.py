# ece_18240.py
# Irene Lin iwl@andrew.cmu.edu
# data_set = students who took 18240
# partition by which semester they took 18240
# map when other cores were taken
# map which other area/coverage courses were taken

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib

GRADE_arr = ["1", "2", "3", "4"]
SEMESTER_arr = ["F", "S"]
STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER


data_arr = lib.parseFile("data/18240_data.csv")

# returns a list of students who took a certrain course
# during a specific grade and semester
def getIdListByCourseGradeSemester(data_arr, course, grade, semester):
    res = []
    for row in data_arr:
        if (course==row[COURSE] and grade==row[GRADE] and semester==row[SEMESTER][0]):
            res.append(row[STUDENT_ID])
    return res

# return all schedule data for students who took a certain course
# during a specific grade and semester
# data_arr  2D list of schedule data
# course    course number string
# grade     class (fr/so/jr/sr)
# semester  fall/spring
def partitionByCourseGradeSemester(data_arr, course, grade, semester):
    id_list = getIdListByCourseGradeSemester(data_arr, course, grade, semester)
    student_data = lib.partitionDataById(id_list, data_arr)
    return student_data

# returns a graph of when other core classes were taken
# nodes are unique by course, grade, and semester
# data_arr  2D list schedule data partitioned by course, grade, and semester
# core      string core class number excluded from graph, common denominator in network
def buildCoreNetwork(data_arr, core):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[STUDENT_ID] == id):
            #same student, add course to array
            if (row[COURSE] in lib.CORE and row[COURSE] != core):
                courses_arr.append(row[COURSE][2:]+row[SEMESTER][0]+row[GRADE])
        else:
            #diff student
            G = lib.addWeightedEdges(G,courses_arr)
            #update id, clear arr
            id = row[STUDENT_ID]
            courses_arr = []
    print(nx.info(G))
    return G

# returns a list of node names with specific prefix
# G graph
# prefix - string to search for
def getNodesWithPrefix(G, prefix):
    res = []
    for n in nx.nodes(G):
        if (n[:len(prefix)] == prefix): res.append(n)
    return res

# returns a list of nodes in a graph that are in a specific set of courses
# G graph
# course_set set of courses for area or concentration
def getNodeinSet(G, course_set):
    res = []
    for n in nx.nodes(G):
        if (n in course_set): res.append(n)
    return res

# course    course number string
# grade     class (fr/so/jr/sr)
# sem       fall/spring
def writeCoreNetwork(data_arr, course, grade, sem):
    student_data = partitionByCourseGradeSemester(data_arr, course, grade, sem)
    G = buildCoreNetwork(student_data, course)
    lib.writeGraph(G, 'networks/core/' + course + sem + grade + '_weighted.edgelist')

def drawCoreNetwork(course, grade, sem):
    G = lib.readGraph('networks/core/' + course + sem + grade + '_weighted.edgelist')
    pos=nx.spring_layout(G,scale=10)
    for e in nx.edges(G):
        nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.05)
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodesWithPrefix(G, "213"),node_size=400, node_color='#66ffff', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodesWithPrefix(G, "220"),node_size=400, node_color='#99ff66', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodesWithPrefix(G, "240"),node_size=400, node_color='#ff6666', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodesWithPrefix(G, "290"),node_size=400, node_color='#cc66ff', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.title(' '.join([course, sem, grade]))
    plt.show()

# returns a graph of when area coverage and classes were taken
# nodes are unique by course, grade, and semester
# data_arr  2D list schedule data partitioned by course, grade, and semester
# core      string core class number excluded from graph, common denominator in network
def buildAreaCoverageNetwork(data_arr, core):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[STUDENT_ID] == id):
            #same student, add course to array
            if ((row[COURSE] in lib.AREA) or (row[COURSE] in lib.COVERAGE)):
                courses_arr.append(row[COURSE])
        else:
            #diff student
            G = lib.addWeightedEdges(G,courses_arr)
            #update id, clear arr
            id = row[STUDENT_ID]
            courses_arr = []
    print(nx.info(G))
    return G

def writeAreaCoverageNetwork(data_arr, course, grade, sem):
    student_data = partitionByCourseGradeSemester(data_arr, course, grade, sem)
    G = buildAreaCoverageNetwork(student_data, course)
    lib.writeGraph(G, 'networks/area_coverage/' + course + sem + grade + '_weighted.edgelist')

def drawAreaCoverageNetwork(course, grade, sem):
    G = lib.readGraph('networks/area_coverage/' + course + sem + grade + '_weighted.edgelist')
    pos=nx.spring_layout(G,scale=10)
    for e in nx.edges(G):
        nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.05)
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodeinSet(G,lib.DEVICES),node_size=400, node_color='#66ffff', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodeinSet(G,lib.CIRCUITS),node_size=400, node_color='#99ff66', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodeinSet(G,lib.HARDWARE),node_size=400, node_color='#ffff00', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodeinSet(G,lib.SOFTWARE),node_size=400, node_color='#ff9999', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getNodeinSet(G,lib.SIGNALS),node_size=400, node_color='#9999ff', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.title(' '.join([course, sem, grade]))
    plt.show()
# for course in lib.CORE:
#     for grade in GRADE_arr:
#         for sem in SEMESTER_arr:
#             writeCoreNetwork(data_arr, course, grade, sem)
# for course in lib.CORE:
#     for grade in GRADE_arr:
#         for sem in SEMESTER_arr:
#             writeAreaCoverageNetwork(data_arr, course, grade, sem)
# drawCoreNetwork('18240', '2', 'S')

for course in lib.CORE:
    for grade in GRADE_arr:
        for sem in SEMESTER_arr:
            drawCoreNetwork(course, grade, sem)
            drawAreaCoverageNetwork(course, grade, sem)
