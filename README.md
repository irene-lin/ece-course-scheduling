# Scripts

### ece_curriculum_library.py
* Helper functions and constants used in various files.

### ece_core_degree_rank.py
* Builds a network with students as nodes and an edge is drawn between two students if they took the same order of core classes. Only students who have taken all four core classes are included in this graph.
* Draws a degree rank plot of students with rank on the x axis and degree on the y axis.
* Draws degree rank plots and highlights students who took area and coverage courses with many prerequisites.

### hard_to_reach_boxplots.py
* Extends 1_ece_core_degree_rank.py
* Draws box plots of node degree for students who took area and coverage courses with many prerequisites.

### ece_cores_communities.py
* Outputs which cores were taken in the same semester by a student and how many students took both cores in that semester.
* Builds a weighted graph with students as nodes and a weighted edge is drawn between students representing the number of core classes taken at the same time.

### area_cov_degree_rank.py
* Builds a network with students as nodes and an edge is drawn between two students if they took the same area or coverage course. Only students who have taken 4 or more area and coverage courses are included in this graph.
* Draws a degree rank plot of students with rank on the x axis and degree on the y axis.
* Draws a degree rank plot of students with rank on the x axis and degree on the y axis and highlights students who took their core classes in a unique order.

### doublemajor.py
* Extends ece_core_degree_rank.py and 2_area_cov_degree_rank.py
* Draws degree rank plots of core class ordering with student node degree on the x axis and degree on the y axis and highlights students who pursued a double major in BME/EPP/Robotics.
* Draws box plots of node degree of core class ordering for students who pursued a double major in BME/EPP/Robotics.
* Draws degree rank plots of area and coverage courses taken with student node degree on the x axis and degree on the y axis and highlights students who pursued a double major in BME/EPP/Robotics.
* Draws box plots of node degree of area and coverage courses taken for students who pursued a double major in BME/EPP/Robotics.

### ece_capstone.py
* Builds a network of students who took capstone in the same academic year and draw an edge between two nodes if two students took the same area or coverage course.

### ece_area_communities.py
* Builds a network or students and draws an edge between two students if they have n or more area/coverage courses in common where n is a parameter for similarity threshold.

### ece_concentration_analysis.py
* For each concentration, builds a list of students who took two or more area courses in that concentration. This list is saved and loaded as a text file.
* Builds a graph of all students and draws an edge between two students if they have the same primary concentration(s). This network shows how closely two concentrations are related.
* Builds core ordering graphs. Nodes are students who are in the same concentration(s) bucket. An edge is drawn between two students who took the same order of core classes. Generates degree rank plots for interesting concentration combinations.
* For each concentration, builds a network of all students in that concentration and draws an edge between two students if they took the same course outside of that concentration.

# Graphs

### cores.gephi
* Core class ordering network.
* Nodes are students and edges are drawn between students who took their core classes in the same order.

### concentrations.gephi
* Secondary area concentration networks.
* One workspace per concentration: 5 workspaces total
* Nodes are students and edges are area/coverage courses in common.
