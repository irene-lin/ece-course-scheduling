# ece_curriculum_library.py
# Irene Lin iwl@andrew.cmu.edu
# This file analyzes the ece undergraduate concentrations.
# If a student took a course in a particular concentration,
# what other courses did they take?

import os
import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib

#build student schedule array
#returns graph G
def buildNetwork(data_arr):
    id = 1
    courses_arr = []
    G = nx.Graph()
    for row in data_arr:
        if (row[0] == id):
            #same student, add course to array
            if (row[1] in lib.AREA or row[1] in lib.COVERAGE):
                courses_arr.append(row[1])
        else:
            #diff student
            G = lib.addWeightedEdges(G,courses_arr)
            #update id, clear arr
            id = row[0]
            courses_arr = []
    print(nx.info(G))
    return G

#draw graph G
# input string title of graph
# input list concentration_course_list - which nodes should be colored differently
def drawNetwork(G, title, concentration_course_list):
    pos=nx.spring_layout(G,scale=10)
    for e in nx.edges(G):
        nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.05)
    nx.draw_networkx_nodes(G,pos,node_size=400, node_color='#dddddd', node_shape='o')
    nx.draw_networkx_nodes(G,pos,nodelist=concentration_course_list,node_size=400, node_color='#ffcc00', node_shape='o')
    nx.draw_networkx_labels(G,pos,font_size=6)
    plt.axis('off')
    plt.title(title)
    plt.show()

def getDevicesGraph():
    devices_data_arr = lib.parseFile("data\devices_concentration_data.csv")
    devices_G = buildNetwork(devices_data_arr)
    return devices_G

def drawDeviceGraph():
    devices_G = lib.readGraph('networks/devices_weighted.edgelist')
    drawNetwork(devices_G,"Devices Concentration Network",list(lib.DEVICES))

def getCircuitsGraph():
    circuits_data_arr = lib.parseFile("data\circuits_concentration_data.csv")
    circuits_G = buildNetwork(circuits_data_arr)
    return circuits_G

def drawCircuitsGraph():
    circuits_G = lib.readGraph('networks/circuits_weighted.edgelist')
    drawNetwork(circuits_G,"Circuits Concentration Network",list(lib.CIRCUITS))

def getHardwareGraph():
    hardware_data_arr = lib.parseFile("data\hardware_concentration_data.csv")
    hardware_G = buildNetwork(hardware_data_arr)
    return hardware_G

def drawHardwareGraph():
    hardware_G = lib.readGraph('networks/hardware_weighted.edgelist')
    drawNetwork(hardware_G,"Hardware Concentration Network",list(lib.HARDWARE))

def getSoftwareGraph():
    software_data_arr = lib.parseFile("data\software_concentration_data.csv")
    software_G = buildNetwork(software_data_arr)
    return software_G

def drawSoftwareGraph():
    software_G = lib.readGraph('networks/software_weighted.edgelist')
    drawNetwork(software_G,"Software Concentration Network",list(lib.SOFTWARE))

def getSignalsGraph():
    signals_data_arr = lib.parseFile("data\signals_concentration_data.csv")
    signals_G = buildNetwork(signals_data_arr)
    return signals_G

def drawSignalsGraph():
    signals_G = lib.readGraph('networks/signals_weighted.edgelist')
    drawNetwork(signals_G,"Signals Concentration Network",list(lib.SIGNALS))


# lib.writeGraph(getDevicesGraph(), 'networks/devices_weighted.edgelist')
# lib.writeGraph(getCircuitsGraph(), 'networks/circuits_weighted.edgelist')
# lib.writeGraph(getHardwareGraph(), 'networks/hardware_weighted.edgelist')
# lib.writeGraph(getSoftwareGraph(), 'networks/software_weighted.edgelist')
# lib.writeGraph(getSignalsGraph(), 'networks/signals_weighted.edgelist')

# drawDeviceGraph()
# drawCircuitsGraph()
# drawHardwareGraph()
# drawSoftwareGraph()
# drawSignalsGraph()
