# ece_curriculum_library.py
# Irene Lin iwl@andrew.cmu.edu
# This file contains helper functions used across all build and analysis files.
# This file also contains constants.

import networkx as nx

# constants
DEVICES = {"18300", "18310", "18403", "18416"}
SIGNALS = {"18370", "18372", "18418", "18491", "18792", "18793", "18794"}
CIRCUITS = {"18320", "18421", "18422"}
HARDWARE = {"18340", "18341", "18447"}
SOFTWARE = {"18330", "18349", "18441", "18452", "15410", "15411", "15415",
            "15418", "15440", "15441", "15445", "15462", "17437"}

COVERAGE = {"15210", "15312", "15281", "15394", "15410", "15411", "15412",
            "15415", "15418", "15440", "15441", "15445", "15451", "15453",
            "15462", "15463", "15466", "16384", "16385", "17214", "17313",
            "17437"}
CORE = ["18213", "18220", "18240", "18290"]

AREA = DEVICES.union(SIGNALS.union(CIRCUITS.union(HARDWARE.union(SOFTWARE))))
AREA_COV = AREA.union(COVERAGE)

#array indices
STUDENT_ID = 0
COURSE = 1
GRADE = 2
SEMESTER = 3

# given a path to a csv file, returns 2D array
def parseFile(infile):
    f_in = open(infile, "r")
    txt_in = f_in.read()
    f_in_arr = txt_in.split("\n")[:-1]
    f_in.close()
    res = []
    for line in f_in_arr:
        res.append(line.split(","))
    return res

#given a 2D array, writes a csv to outfile
def writeFile(outfile, arr):
    f_out = open(outfile, "w")
    for i in arr:
        f_out.write(",".join(i))
        f_out.write("\n")
    f_out.close()

# returns a list of students who took a specific course
def getIdListByCourse(data_arr, course, only_ugrad=False):
    res = []
    for row in data_arr:
        if (row[COURSE] == course):
            if (row[STUDENT_ID] not in res):
                if (only_ugrad == True):
                    if(int(row[GRADE]) <= 4): res.append(row[STUDENT_ID])
                else:
                    res.append(row[STUDENT_ID])
    return res

# return all schedule data for every student in id_arr
def partitionDataById(id_arr, data_arr):
    res = []
    for row in data_arr:
        if (row[STUDENT_ID] in id_arr):
            res.append(row)
    return res

# get schedules for all students who have taken a specific course and write to file
def writeCoursePartition(course):
    data_arr = parseFile('data/ECE_Student_Data_Request_9.25.19.csv')
    student_id_arr = getIdListByCourse(data_arr, course)
    student_data = partitionDataById(student_id_arr, data_arr)
    writeFile('data/'+course+'_data.csv', student_data)

# get schedules for all students who have taken any course
# in a specific concentration and write to file
# input course_set is set of courses pertaining to one concentration
def writeConcentrationPartition(course_set, concentration_name):
    data_arr = parseFile('data/ECE_Student_Data_Request_9.25.19.csv')
    student_id_arr = []
    for course in course_set:
        student_id_arr += getIdListByCourse(data_arr, course)
    student_data = partitionDataById(student_id_arr, data_arr)
    writeFile('data/'+concentration_name+'_concentration_data.csv', student_data)

def getFrequencyList():
    data_arr = parseFile('data/ECE_Student_Data_Request_9.25.19.csv')
    d = dict()
    for row in data_arr:
        c = row[COURSE]
        if (c in d): d[c] += 1
        else: d[c] = 1
    #convert to list of tuples
    arr = []
    for c in d:
        arr.append((c, d[c]))
    sorted_by_second = sorted(arr, key=lambda tup: tup[1], reverse=True)
    # for tup in sorted_by_second:
    #     if (tup[0][:2] in {'18', '15', '17'}):
    #         print(tup)
    return sorted_by_second

# returns a list of nodes in a graph that are in a specific set of courses
# G graph
# course_set set of courses for area or concentration
def getNodeinSet(G, course_set):
    res = []
    for n in nx.nodes(G):
        if (n in course_set): res.append(n)
    return res
# ----------------------------------------------------------------------------
# ANALYSIS FUNCTIONS

def writeGraph(G,outfile):
    nx.write_weighted_edgelist(G, outfile)

def readGraph(infile):
    return nx.read_weighted_edgelist(infile)

# draws an edge between every combination of courses in courses_arr
# courses_arr   list of nodes to draw edges between, entire list should belong to one student
def addWeightedEdges(G,courses_arr):
    # iterate through every combination
    if (len(courses_arr) == 1): G.add_node(courses_arr[0])
    for i in range(len(courses_arr)):
        for j in range(i+1, len(courses_arr)):
            course1 = courses_arr[i]
            course2 = courses_arr[j]
            #increment course weight if already in network
            if ((course1, course2) in nx.edges(G)):
                new_weight = G[course1][course2]['weight'] + 1
                G.add_edge(course1, course2, weight=new_weight)
            #add to network with weight 1
            else:
                G.add_edge(course1, course2, weight=1)
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

# input infile is path to edgelist
# input outfile is path to csv
def edgelistToCSV(infile, outfile):
    f_in = open(infile, "r")
    txt_in = f_in.read()
    f_in_arr = txt_in.split("\n")[:-1]
    f_in.close()
    f_out = open(outfile, "w")
    f_out.write("Source,Target,Weight\n")
    for line in f_in_arr:
        f_out.write(','.join(line.split()))
        f_out.write("\n")
    f_out.close()

def getNodeCentralitySorted(G):
    d = nx.betweenness_centrality(G)
    a = []
    for node in d:
        a.append((node,d[node]))
    return sorted(a, key=lambda tup: tup[1], reverse=True)

def getEdgeCentralitySorted(G):
    d = nx.edge_betweenness_centrality(G)
    a = []
    for edge in d:
        a.append((edge,d[edge]))
    return sorted(a, key=lambda tup: tup[1], reverse=True)
