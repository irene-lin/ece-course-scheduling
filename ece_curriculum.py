import os
import networkx as nx
import matplotlib.pyplot as plt
import ece_curriculum_library as lib



def add_weighted_edges(G,courses_arr):
    # iterate through every combination
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



#-------------------------------------------------------------------------------



# read data (id, course, grade, semester)
print(os.listdir())
data_arr = lib.parseFile('data/ECE_Student_Data_Request_9.25.19.csv')

# get set of courses
course_set = set()
for row in data_arr:
    course_set.add(row[1])
course_set = sorted(course_set)

# build weighted graph: nodes are courses, edges are students
id = 1
courses_arr = []
G = nx.Graph()
for row in data_arr:
    if (row[0] == id):
        #same student, add course to array
        if (row[1][0]=='1' and (row[1] in lib.AREA or row[1] in lib.COVERAGE)):
            courses_arr.append(row[1])
    else:
        #diff student
        G = add_weighted_edges(G,courses_arr)
        #update id, clear arr
        id = row[0]
        courses_arr = []
print(nx.info(G))

pos=nx.spring_layout(G)
for e in nx.edges(G):
    nx.draw_networkx_edges(G,pos,edge_color='b', edgelist=[e],width=G[e[0]][e[1]]['weight']*.05)
nx.draw_networkx_labels(G,pos,font_size=5,font_family='sans-serif', node_size=50)
plt.axis('off')
plt.show()
