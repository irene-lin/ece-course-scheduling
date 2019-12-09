# doublemajor.py
# Irene Lin iwl@andrew.cmu.edu
# Draws degree rank plots of core class ordering with student node degree on
# the x axis and degree on the y axis and highlights students who pursued a
# double major in BME/EPP/Robotics.
# Draws box plots of node degree of core class ordering for students who pursued
# a double major in BME/EPP/Robotics.
# Draws degree rank plots of area and coverage courses taken with student node
# degree on the x axis and degree on the y axis and highlights students who
# pursued a double major in BME/EPP/Robotics.
# Draws box plots of node degree of area and coverage courses taken for students
# who pursued a double major in BME/EPP/Robotics.

import networkx as nx
import ece_curriculum_library as lib
import ece_core_degree_rank as core
import area_cov_degree_rank as area_cov
import matplotlib.pyplot as plt

STUDENT_ID = lib.STUDENT_ID
COURSE = lib.COURSE
GRADE = lib.GRADE
SEMESTER = lib.SEMESTER

"""
BIOMEDICAL ENGINEERING CASTONE COURSES
- 42401 Foundation of BME Design
- 42402 BME Design Project

ENGINEERING & PUBLIC POLICY CAPSTONE COURSES
- 19351 Applied Methods for Technology-Policy Analysis
- 19451 EPP Projects I
- 19452 EPP Projects II

ROBOTICS CAPSTONE COURSE
- 16474 Robotics Capstone
"""

# get 2D array of student data
data_arr = lib.parseFile("data/ECE_Student_Data_Request_9.25.19.csv")

# helper function for drawBoxPlots()
def getDegreeRankDataset(G, course_list):
    id_list = []
    for c in course_list:
        id_list += lib.getIdListByCourse(data_arr, c, only_ugrad=True)
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
    ranks_BME = getDegreeRankDataset(G, ['42401', '42402'])
    ranks_EPP = getDegreeRankDataset(G, ['19351', '19451', '19452'])
    ranks_ROB = getDegreeRankDataset(G, ['16474'])

    fig, ax = plt.subplots()
    box_plot_data=[ranks_BME, ranks_EPP, ranks_ROB]
    box = plt.boxplot(box_plot_data, vert=1, patch_artist=True, labels=['BME','EPP','ROB'])
    plt.title(title)
    plt.xlabel('Degree')
    plt.ylabel('Double Major')
    colors = ['lime', 'cyan', 'yellow']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

# helper function for drawDegreeRankPlot()
def getDataset(G, course_list):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = []
    y = []
    id_list = []
    for c in course_list:
        id_list += lib.getIdListByCourse(data_arr, c, only_ugrad=True)
    for i in range(len(deg_sorted)):
        id,deg = deg_sorted[i]
        if id in id_list:
            x.append(i)
            y.append(deg)
    return (x,y)

def drawDegreeRankPlot(G, title):
    deg_sorted = sorted(nx.degree(G), key=lambda tup: tup[1], reverse=True)
    x = [i for i in range(len(deg_sorted))]
    y = [b for (a,b) in deg_sorted]
    (x1, y1) = getDataset(G, ['16474'])
    (x2, y2) = getDataset(G, ['19351', '19451', '19452'])
    (x3, y3) = getDataset(G, ['42401', '42402'])

    plt.subplot(3,1,1)
    plt.scatter(x, y, c='black')
    plt.scatter(x1, y1, c='yellow', label='Students who took \nROB Capstone')
    plt.legend(loc='lower left')
    plt.title(title)
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(3,1,2)
    plt.scatter(x, y, c='black')
    plt.scatter(x2, y2, c='cyan', label='Students who took \nEPP Capstone')
    plt.legend(loc='lower left')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

    plt.subplot(3,1,3)
    plt.scatter(x, y, c='black')
    plt.scatter(x3, y3, c='lime', label='Students who took \nBME Capstone')
    plt.legend(loc='lower left')
    plt.xlabel('Rank')
    plt.ylabel('Degree')

d1 = core.getDictionaryCoreClassOrdering(data_arr)
G1 = core.buildCoreOrderingGraph(data_arr, d1)
drawDegreeRankPlot(G1, 'Degree Rank Plot for Core Class Ordering')
drawBoxPlots(G1, 'Box Plots Double Major Students Core Class Ordering')

d2 = area_cov.getDictionaryAreaCoverage(data_arr)
G2 = area_cov.buildAreaCoverageGraph(data_arr, d2)
drawDegreeRankPlot(G2, 'Degree Rank Plot for Area & Coverage Courses')
drawBoxPlots(G2, 'Box Plots Double Major Students Area and Coverage Courses')
