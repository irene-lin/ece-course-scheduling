# hard_to_reach_boxplots.py
# Irene Lin iwl@andrew.cmu.edu
# Draws box plots of node degree for students who took area and coverage courses 
# with many prerequisites.

import networkx as nx
import ece_curriculum_library as lib
import ece_core_degree_rank as core
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

def getDegreeRankDataset(G, course):
    id_list = lib.getIdListByCourse(data_arr, course, only_ugrad=True)
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    ranks = []
    for i in range(len(deg_sorted)):
        id,deg = deg_sorted[i]
        if id in id_list:
            ranks.append(deg)
    return ranks

def drawBoxPlots(G, title):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    y = [b for (a,b) in deg_sorted]
    ranks_422 = getDegreeRankDataset(G, '18422')
    ranks_421 = getDegreeRankDataset(G, '18421')
    ranks_792 = getDegreeRankDataset(G, '18792')
    ranks_451 = getDegreeRankDataset(G, '15451')

    fig, ax = plt.subplots()
    box_plot_data=[ranks_422, ranks_421, ranks_792, ranks_451]
    box = plt.boxplot(box_plot_data, vert=1, patch_artist=True, labels=['18422','18421','18792','15451'])
    plt.title(title)
    plt.xlabel('Degree')
    plt.ylabel('Course')
    colors = ['cyan', 'yellow', 'lime', 'red']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

d = core.getDictionaryCoreClassOrdering(data_arr)
G = core.buildCoreOrderingGraph(data_arr, d)
drawBoxPlots(G, 'Box Plots for Core Class Orderings')
