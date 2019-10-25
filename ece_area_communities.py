# ece_area_communities.py
# Irene Lin iwl@andrew.cmu.edu

#nodes are students, edges are classes taken together


import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib
import ece_cores as cores

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
        if (line[COURSE] in lib.AREA):# and line[COURSE] not in COMMON_AREA):
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

#for all students in dictionary, draw weighted edges to every other student that took a similar course
def buildGraph(data_arr, intersection_size):
    G = nx.Graph()
    d = getDictionary(data_arr)
    for i in range(1,5057+1):
        for j in range(i+1, 5057+1):
            (id1, id2) = (str(i), str(j))
            if (id1 in d and id2 in d):
                course_set1 = d[id1]
                course_set2 = d[id2]
                intersection = course_set1.intersection(course_set2)
                if (len(intersection) >= intersection_size):
                    G.add_edge(id1, id2, weight=len(intersection))
    print(nx.info(G))
    return G

def writeCoreNetwork(data_arr, intersection_size):
    G = buildGraph(data_arr, intersection_size)
    lib.writeGraph(G, getEdgelistPath(FILEPATH_AREA, str(intersection_size)))
    lib.edgelistToCSV(getEdgelistPath(FILEPATH_AREA, str(intersection_size)),
                                            getCSVPath(FILEPATH_AREA, str(intersection_size)))

def drawNetwork(data_arr, intersection_size):
    G = lib.readGraph(getEdgelistPath(FILEPATH_AREA, str(intersection_size)))
    pos=nx.spring_layout(G,scale=10)
    nx.draw_networkx_edges(G,pos,edge_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=5)
    plt.axis('off')
    plt.show()

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


# drawNetwork(data_arr, 3)

d = getDictionary(data_arr)
# print(d['372'].intersection(d['921']))
# print(d['372'].intersection(d['2300']))
# print(d['921'].intersection(d['2300']))
print(2897, d['2897'])
print(846, d['846'])
print(1116, d['1116'])

print(d['846'].intersection(d['3449']))
print(d['1116'].intersection(d['3449']))
print(d['846'].intersection(d['2897']))

# for i in range (2,7):
#     writeCoreNetwork(data_arr, i)
# intersection_size = 5
# G = lib.readGraph(getEdgelistPath(FILEPATH_AREA, str(intersection_size)))
# print(getNodeCentralitySorted(G))
# print(getEdgeCentralitySorted(G))
# print(2897, d['2897'], 846, d['846'], 1116, d['1116'])
