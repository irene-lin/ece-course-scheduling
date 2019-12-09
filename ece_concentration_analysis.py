# ece_concentration_analysis.py
# Irene Lin iwl@andrew.cmu.edu
# For each concentration, builds a list of students who took two or more area
# courses in that concentration. This list is saved and loaded as a text file.
# Builds a graph of all students and draws an edge between two students if they
# have the same primary concentration(s). This network shows how closely two
# concentrations are related.
# Builds core ordering graphs. Nodes are students who are in the same
# concentration(s) bucket. An edge is drawn between two students who took the
# same order of core classes. Generates degree rank plots for interesting
# concentration combinations.
# For each concentration, builds a network of all students in that concentration
# and draws an edge between two students if they took the same course outside of
# that concentration.

import numpy as np
import networkx as nx
import ece_curriculum_library as lib
import matplotlib.pyplot as plt
import ece_core_degree_rank as cores

f_student_data = "data/ECE_Student_Data_Request_9.25.19.csv"
data_arr_ = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")
data_arr = np.genfromtxt(f_student_data, delimiter=',', dtype='U5')

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

student_id_arr = data_arr[:,STUDENT_ID].astype(int)
student_id_arr = np.reshape(student_id_arr, (-1, 1))
course_arr = data_arr[:,COURSE]
course_arr = np.reshape(course_arr, (-1, 1))
grade_arr = data_arr[:,GRADE].astype(int)
grade_arr = np.reshape(grade_arr, (-1, 1))
sem_arr = data_arr[:,SEMESTER]
sem_arr = np.reshape(sem_arr, (-1, 1))

def getCourseConcentrationDict():
    d = dict()
    for c in lib.DEVICES:
        d[c] = 'dev'
    for c in lib.SIGNALS:
        d[c] = 'sig'
    for c in lib.CIRCUITS:
        d[c] = 'cir'
    for c in lib.HARDWARE:
        d[c] = 'hw'
    for c in lib.SOFTWARE:
        d[c] = 'sw'
    for c in lib.COVERAGE:
        d[c] = 'cov'
    return d

# returns a set of all area and coverage courses for a specific student id
def getAreaCovScheduleSet(id):
    id = str(id)
    #get indicies of data rows with STUDENT_ID = id
    data_rows = np.where(data_arr[:,STUDENT_ID]==id)
    s = set()
    for row_i in data_rows[0]:
        c = data_arr[row_i][COURSE]
        if (c in lib.AREA_COV):
            s.add(c)
    return s

#returns a list of student ids of all students who took 4 or more area/coverage
# courses and took at least two courses in the concentration_set
def getStudentsInConcentration(concentration_set):
    # get last student id
    max_id = np.amax(student_id_arr)
    id_list = []
    # iterate through all students
    for id in range(max_id+1):
        # get set of area and coverage courses for student
        s = getAreaCovScheduleSet(id)
        # if student took at least two courses in the concentration_set and
        # at least 4 area/coverage courses, add to result
        if (len(s.intersection(concentration_set)) >= 2 and len(s) >= 4):
            id_list.append(id)
    return id_list

# saves id lists for students who took 4 or more area/coverage
# courses and took at least two courses in the concentration_set
def saveConcentrationIdLists():
    np.savetxt('concentration_id_lists/id_list_DEVICES.txt', getStudentsInConcentration(lib.DEVICES), fmt="%d")
    np.savetxt('concentration_id_lists/id_list_CIRCUITS.txt', getStudentsInConcentration(lib.CIRCUITS), fmt="%d")
    np.savetxt('concentration_id_lists/id_list_HARDWARE.txt', getStudentsInConcentration(lib.HARDWARE), fmt="%d")
    np.savetxt('concentration_id_lists/id_list_SOFTWARE.txt', getStudentsInConcentration(lib.SOFTWARE), fmt="%d")
    np.savetxt('concentration_id_lists/id_list_SIGNALS.txt', getStudentsInConcentration(lib.SIGNALS), fmt="%d")

devices_id_list = np.loadtxt('concentration_id_lists/id_list_DEVICES.txt', dtype="i8")
circuits_id_list = np.loadtxt('concentration_id_lists/id_list_CIRCUITS.txt', dtype="i8")
hardware_id_list = np.loadtxt('concentration_id_lists/id_list_HARDWARE.txt', dtype="i8")
software_id_list = np.loadtxt('concentration_id_lists/id_list_SOFTWARE.txt', dtype="i8")
signals_id_list = np.loadtxt('concentration_id_lists/id_list_SIGNALS.txt', dtype="i8")
dev_set = set(devices_id_list)
cir_set = set(circuits_id_list)
hw_set = set(hardware_id_list)
sw_set = set(software_id_list)
sig_set = set(signals_id_list)

# Devices Circuits Hardware Software Signals
def printSetIntersectionLengths():
    max_id = np.amax(student_id_arr)
    all = set([i for i in range(max_id+1)])

    for i in range(1,32):
        (s1, s2, s3, s4, s5) = (all, all, all, all, all)
        if (i&1): s1 = sig_set
        if (i&2): s2 = sw_set
        if (i&4): s3 = hw_set
        if (i&8): s4 = cir_set
        if (i&16): s5 = dev_set

        intersection = s1.intersection(s2).intersection(s3).intersection(s4).intersection(s5)
        s = len(intersection)
        if (s > 0):
            print(s, end="\t")
            if (len(s5) < len(all)): print("devices", end=" ")
            if (len(s4) < len(all)): print("circuits", end=" ")
            if (len(s3) < len(all)): print("hardware", end=" ")
            if (len(s2) < len(all)): print("software", end=" ")
            if (len(s1) < len(all)): print("signals", end=" ")
            print(intersection)

# add edge from every id to every other id in the list
def addEdges(G, id_list, tag):
    for i in range(len(id_list)):
        id1=id_list[i]
        G.add_node(id1, label=tag)
        for j in range(i+1,len(id_list)):
            id2 = id_list[j]
            G.add_edge(id1, id2, label=tag, weight=len(tag.split("-")))
    return G

#draws an edge between two students if they are in the same concentration bucket
def buildConcentrationGroupsGraph():
    G = nx.Graph()
    #add nodes in order from least to most intersections

    # one concentration
    addEdges(G, devices_id_list, "dev")
    addEdges(G, circuits_id_list, "cir")
    addEdges(G, hardware_id_list, "hw")
    addEdges(G, software_id_list, "sw")
    addEdges(G, signals_id_list, "sig")

    # two concentrations
    addEdges(G, list(dev_set.intersection(cir_set)), "dev-cir")
    addEdges(G, list(dev_set.intersection(hw_set)), "dev-hw")
    addEdges(G, list(dev_set.intersection(sw_set)), "dev-sw")
    addEdges(G, list(dev_set.intersection(sig_set)), "dev-sig")

    addEdges(G, list(cir_set.intersection(hw_set)), "cir-hw")
    addEdges(G, list(cir_set.intersection(sw_set)), "cir-sw")
    addEdges(G, list(cir_set.intersection(sig_set)), "cir-sig")

    addEdges(G, list(hw_set.intersection(sw_set)), "hw-sw")
    addEdges(G, list(hw_set.intersection(sig_set)), "hw-sig")

    addEdges(G, list(sw_set.intersection(sig_set)), "sw-sig")

    # three concentrations
    addEdges(G, list(hw_set.intersection(sw_set).intersection(sig_set)), "hw-sw-sig")
    addEdges(G, list(dev_set.intersection(cir_set).intersection(sig_set)), "dev-cir-sig")
    addEdges(G, list(cir_set.intersection(hw_set).intersection(sw_set)), "cir-hw-sw")
    addEdges(G, list(dev_set.intersection(hw_set).intersection(sw_set)), "dev-hw-sw")

    f = open("networks/concentrations_areacov_nodes.csv", 'w')
    f.write("Id Label\n")
    for n in G.nodes():
        f.write("%d %s\n"%(n, G.node[n]['label']))

    return G

def addNodes(G,n,tag):
    if (G.has_node(n)):
        G.nodes[n]['label'] = G.nodes[n]['label'] + '-' + tag
    else:
        G.add_node(n, label=tag)
    return G
#draw edge between two students if they took the same area or coverage course
# only include students who have taken 4+ area/coverage courses and 2+ courses in one area
def buildConcentrationGraph():
    id_list = list(dev_set.union(cir_set).union(hw_set).union(sw_set).union(sig_set))
    G = nx.Graph()
    for id in devices_id_list:
        G = addNodes(G, id, 'dev')
    for id in circuits_id_list:
        G = addNodes(G, id, 'cir')
    for id in hardware_id_list:
        G = addNodes(G, id, 'hw')
    for id in software_id_list:
        G = addNodes(G, id, 'sw')
    for id in signals_id_list:
        G = addNodes(G, id, 'sig')

    course_concentration_mapping = getCourseConcentrationDict()
    for i in range(len(id_list)):
        id1 = id_list[i]
        s1 = getAreaCovScheduleSet(id1)
        for j in range(i+1, len(id_list)):
            id2 = id_list[j]
            s2 = getAreaCovScheduleSet(id2)
            intersection = s1.intersection(s2)
            if (len(intersection) > 0):
                G.add_edge(id1,id2,weight=len(intersection))
    # write edges with weight and label
    f = open("networks/concentrations_areacov_edgelist_all.csv", 'w')
    f.write("Source Target Weight\n")
    for e in G.edges(data=True):
        f.write("%d %d %d\n"%(e[0], e[1], e[2]['weight']))
    f.close()
    # write nodes with label
    f = open("networks/concentrations_areacov_nodes_all.csv", 'w')
    f.write("Id Label\n")
    for n in G.nodes():
        print(n)
        f.write("%d %s\n"%(n, G.node[n]['label']))
    f.close()
    return G
# helper function for drawDegreeRankPlotConcentrations
# returns x and y arrays for plotting
def getDegreeRankDataset(G, id_list):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = []
    y = []
    for rank in range(len(deg_sorted)):
        (id, deg) = deg_sorted[rank]
        if (int(id) in id_list):
            x.append(rank)
            y.append(deg)
    return(x,y)

def drawDegreeRankPlotConcentrations():
    d = cores.getDictionaryCoreClassOrdering(data_arr_)
    G = cores.buildCoreOrderingGraph(data_arr_, d)
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = [i for i in range(len(deg_sorted))]
    y = [b for (a,b) in deg_sorted]


    (x1, y1) = getDegreeRankDataset(G, list(sig_set.intersection(hw_set)))
    (x2, y2) = getDegreeRankDataset(G, list(sig_set.intersection(dev_set)))
    (x3, y3) = getDegreeRankDataset(G, list(cir_set.intersection(hw_set)))
    (x4, y4) = getDegreeRankDataset(G, list(cir_set.intersection(sig_set)))
    (x5, y5) = getDegreeRankDataset(G, list(cir_set.intersection(dev_set)))

    plt.subplot(5,1,1)
    plt.title("Degree Rank Plot for Core Class Orderings")
    plt.scatter(x, y, c='black')
    plt.scatter(x1, y1, c='yellow', label='Hardware & Signals Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(5,1,2)
    plt.scatter(x, y, c='black')
    plt.scatter(x2, y2, c='cyan', label='Devices & Signals Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')


    plt.subplot(5,1,3)
    plt.scatter(x, y, c='black')
    plt.scatter(x3, y3, c='red', label='Circuits & Hardware Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(5,1,4)
    plt.scatter(x, y, c='black')
    plt.scatter(x4, y4, c='lime', label='Circuits & Signals Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(5,1,5)
    plt.scatter(x, y, c='black')
    plt.scatter(x5, y5, c='gray', label='Circuits & Devices Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.show()

    (x1, y1) = getDegreeRankDataset(G, list(sig_set.intersection(sw_set)))
    (x2, y2) = getDegreeRankDataset(G, devices_id_list)
    (x3, y3) = getDegreeRankDataset(G, circuits_id_list)

    plt.subplot(3,1,1)
    plt.scatter(x, y, c='black')
    plt.scatter(x1, y1, c='yellow', label='Software & Signals Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(3,1,2)
    plt.scatter(x, y, c='black')
    plt.scatter(x2, y2, c='lime', label='Devices Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(3,1,3)
    plt.scatter(x, y, c='black')
    plt.scatter(x3, y3, c='cyan', label='Circuits Concentration')
    plt.legend(loc='upper right')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.show()

def buildAreaCoverageGraph(concentration_id_list, concentration_set, name):
    G = nx.Graph()
    course_concentration_mapping = getCourseConcentrationDict()
    for i in range(len(concentration_id_list)):
        n1 = concentration_id_list[i]
        s1 = getAreaCovScheduleSet(n1)
        tag = "-".join(s1)
        G.add_node(n1, label=tag)
        for j in range(i+1, len(concentration_id_list)):
            n2 = concentration_id_list[j]
            s2 = getAreaCovScheduleSet(n2)
            # get all courses in common that are not in concentration_set
            intersection = s1.intersection(s2)
            intersection = intersection.difference(concentration_set)

            if (len(intersection) > 0):
                # generate label for edge
                tag_arr = []
                tag_set = set()
                for c in intersection:
                    tag_set.add(course_concentration_mapping[c])
                tag_arr = list(tag_set)
                tag_arr.sort()
                tag = '-'.join(tag_arr)
                # draw weighted edge
                G.add_edge(n1,n2,weight=len(intersection),label=tag)
    # write edges with weight and label
    f = open("networks/concentrations_areacov_edgelist_%s.csv"%(name), 'w')
    f.write("Source Target Weight Label\n")
    for e in G.edges(data=True):
        f.write("%d %d %d %s\n"%(e[0], e[1], e[2]['weight'], e[2]['label']))
    # write nodes with label
    f = open("networks/concentrations_areacov_nodes_%s.csv"%(name), 'w')
    f.write("Id Label\n")
    for n in G.nodes():
        f.write("%d %s\n"%(n, G.node[n]['label']))
    return G

buildConcentrationGraph()
drawDegreeRankPlotConcentrations()
printSetIntersectionLengths()
buildAreaCoverageGraph(hardware_id_list, lib.HARDWARE, "hardware")
