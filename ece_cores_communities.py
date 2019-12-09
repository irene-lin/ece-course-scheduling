# ece_cores_communities.py
# Irene Lin iwl@andrew.cmu.edu
# Outputs which cores were taken in the same semester by a student and how many
# students took both cores in that semester. Builds a weighted graph with
# students as nodes and a weighted edge is drawn between students representing
# the number of core classes taken at the same time.

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib
import matplotlib.pyplot as plt

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

#get data_set
data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

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
