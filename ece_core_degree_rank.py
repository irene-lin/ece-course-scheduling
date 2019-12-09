# ece_core_degree_rank.py
# Irene Lin iwl@andrew.cmu.edu
# Builds a network with students as nodes and an edge is drawn between two
# students if they took the same order of core classes. Only students who have
# taken all four core classes are included in this graph.
# Draws a degree rank plot of students with rank on the x axis and degree on the
# y axis. Draws degree rank plots and highlights students who took area and
# coverage courses with many prerequisites.

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

# returns x array of node rank if student took specified course
# and y array of corresponding degree
# for highlighting students on degree rank plot
def getDataset(G, course):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = []
    y = []
    id_list = lib.getIdListByCourse(data_arr, course, only_ugrad=True)
    for i in range(len(deg_sorted)):
        id,deg = deg_sorted[i]
        if id in id_list:
            x.append(i)
            y.append(deg)
    return (x,y)

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

def drawDegreeRankPlot(G):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = [i for i in range(len(deg_sorted))]
    y = [b for (a,b) in deg_sorted]
    id_list = getIdListForUniqueCoreOrdering(data_arr)
    x1 = []
    y1 = []
    for rank in range(len(deg_sorted)):
        (id, deg) = deg_sorted[rank]
        if (int(id) in id_list):
            x1.append(rank)
            y1.append(deg)

    colors = ("black")
    fig, ax = plt.subplots()
    plt.scatter(x, y, c='black')
    plt.title('Degree Rank Plot for Core Class Ordering')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = "Nodes: students \nEdges: Same ordering of \nall four core classes"
    # place a text box in upper left in axes coords
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.show()

def drawDegreeRankPlotHardToReach(G):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x1 = [i for i in range(len(deg_sorted))]
    y1 = [b for (a,b) in deg_sorted]
    (x2, y2) = getDataset(G, '15451')
    (x3, y3) = getDataset(G, '18792')
    (x4, y4) = getDataset(G, '18421')
    (x5, y5) = getDataset(G, '18422')

    plt.subplot(2,2,1)
    plt.title('Degree Rank Plots for Core Class Orderings')
    plt.scatter(x1, y1, c="black")
    plt.scatter(x2, y2, c="red", label='Students who took 15451 \nAlgorithm Design and Analysis')
    plt.legend(loc='upper right');
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(2,2,2)
    plt.scatter(x1, y1, c="black")
    plt.scatter(x3, y3, c="lime", label='Students who took 18792 \nAdvanced Digital Signal Processing')
    plt.legend(loc='upper right');
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(2,2,3)
    plt.scatter(x1, y1, c="black")
    plt.scatter(x4, y4, c="yellow", label='Students who took 18421 \nAnalog Integrated Circuit Design')
    plt.legend(loc='upper right');
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(2,2,4)
    plt.scatter(x1, y1, c="black")
    plt.scatter(x5, y5, c="cyan", label='Students who took 18422 \nDigital Integrated Circuit Design')
    plt.legend(loc='upper right');
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.show()

#draw network
def drawCoreNetwork(suffix):
    G = lib.readGraph(getEdgelistPath(cores.FILEPATH_CORE, suffix))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.show()

d = getDictionaryCoreClassOrdering(data_arr)
G = buildCoreOrderingGraph(data_arr, d)
drawDegreeRankPlot(G)
drawDegreeRankPlotHardToReach(G)
