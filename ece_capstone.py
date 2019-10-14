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

def getIdListBySemester(data_arr, semester):
     pass

def buildCapstoneNetwork(data_arr):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[STUDENT_ID] == id and row[COURSE] in CORES and row[SEMESTER] == sem):
            #same student, add course to array
            courses_arr.append(row[1])
        else:
            #diff student
            G = lib.addWeightedEdges(G,courses_arr)
            #update id, clear arr
            id = row[0]
            courses_arr = []
    print(nx.info(G))
    return G
