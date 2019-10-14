# ece_masters.py
# Irene Lin iwl@andrew.cmu.edu

import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib

GRADE_arr = ["1", "2", "3", "4"]
SEMESTER_arr = ["F", "S"]
STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

# Cyber-Physical Systems
CPS = {"18644", "18642", "18648", "18651", "18667", "18745", "18748", "18843",
       "18849", "18771", "18776", "18792", "18793", "18794", "18637", "18638",
       "18730", "18756", "18743", "18781", "18797"}
# Computer Security
CSEC = {"18631", "18730", "18731", "18732", "18733", "18734", "18632", "18635",
        "18636", "18637", "18638", "18765", "18739"}
#Data and Network Science
DNS = {"18660", "18661", "18697", "18751", "18752", "18753", "18754", "18755",
       "18782", "18794", "18651", "18748", "18759", "18618", "18663", "18875",
       "18879", "18698", "18790", "18792", "18793"}
#Integrated Systems Design
ISD = {"18623", "18622", "18664", "18725", "18726", "18721", "18723", "18625",
       "18640", "18742", "18760", "18762", "18765", "18727", "18610", "18614"}
#Wireless Systems
WS = {"18743", "18747", "18846", "18637", "18741", "18748", "18859", "18750",
      "18741", "18744", "18745"}
CONCENTRATIONS = CPS.union(CSEC.union(DNS.union(ISD.union(WS))))

data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")
grad_data_arr = []
for row in data_arr:
    if (row[GRADE]=='10'):
        grad_data_arr.append(row)

#graph all grad courses

def getConcentrationList(G, concentration_set):
    res = []
    for n in concentration_set:
        if n in nx.nodes(G):
            res.append(n)
    return res

#build student schedule array
#returns graph G
def buildGradNetworkAll(data_arr):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[STUDENT_ID] == id and row[COURSE][:2] == '18'):
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

#draw graph G, color each concentration differently
# input string title of graph
def drawGradNetworkAll(G, title):
    pos=nx.spring_layout(G,scale=10)
    for e in nx.edges(G):
        nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.05)
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getConcentrationList(G,CPS),node_size=400, node_color='#ffcc00', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getConcentrationList(G,CSEC),node_size=400, node_color='#ccff00', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getConcentrationList(G,DNS),node_size=400, node_color='#ff00cc', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getConcentrationList(G,ISD),node_size=400, node_color='#cccc00', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=getConcentrationList(G,WS),node_size=400, node_color='#00ccff', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.title(title)
    plt.show()

# G = buildGradNetworkAll(grad_data_arr)
# drawGradNetworkAll(G, 'Graduate Students')

#graph all concentration courses
def buildGradNetworkAllConcentrations(data_arr):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[STUDENT_ID] == id and row[COURSE] in CONCENTRATIONS):
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

G = buildGradNetworkAllConcentrations(grad_data_arr)
drawGradNetworkAll(G, 'Graduate Students, Concentrations only')
