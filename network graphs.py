# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 12:05:53 2016

@author: brian
"""

import networkx as nx
import pandas as pd
import numpy as np
import os
import itertools
import matplotlib.pyplot as plt

os.chdir("C:/Users/Brian/Desktop/MS-BA/03 Spring Semester/Social Media Analytics/sma_assignment 3")
top_brands = pd.read_csv('top brands.csv')
lift_chart = pd.read_csv('lift chart.csv')

top_brands.columns.values
top_brands = top_brands.drop(top_brands.columns[0], axis=1) #getting rid of the index columns from vivian's original output
lift_chart.columns.values
lift_chart = lift_chart.drop(lift_chart.columns[0], axis=1) #same as above, don't need this if the csv lacks a column that says 'Unnamed'

lift_chart.replace(1, np.NaN, inplace=True) #replace diagonals with NaN
lift_chart[lift_chart<2] = 0 #would remove all lift values below 1, IF THERE WERE ANY

brand_names = lift_chart.columns.values
brand_edges = list(itertools.combinations(lift_chart.columns.values,2)) # pairs of brands

G=nx.Graph()
G.add_nodes_from(brand_names)
G.number_of_nodes()
G.add_edges_from(brand_edges)
G.number_of_edges()

#need to index each number using brand_edges pairs to index
lift_chart.index = lift_chart.columns.values
#lift_chart['bmw']['audi'] #it works!
#lift_chart[ brand_edges[0][0] ] [ brand_edges[0][1] ] #this works too!
for i in range(0,len(brand_edges)): #adding all the weights
    G.edge[brand_edges[i][0]][brand_edges[i][1]]['weight'] = lift_chart[brand_edges[i][0]][brand_edges[i][1]]

#drawing a graph
nx.draw(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)

"""
lift_chart.describe() #will use 1-2.5, 2.5-4, and >4
pos=nx.spring_layout(G) # positions for all nodes
nx.draw_networkx_edges(G,pos,edgelist=brand_edges,width=6)
"""

edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)] #list of edge weights
node_labels = {} #creating node labels, needs to be in dictionary
node_names = brand_names
node_names.sort()
for i in range(0,len(brand_names)):
    node_labels[i] = brand_names[i] #node indices starts at 1
    node_labels.sort

pos = nx.spring_layout(G) #generating the note positions
plt.figure(figsize=(20, 40)) #figure size
plt.subplot(211); plt.axis('off') #suplot(211) is a reference to dimensions or something
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, width=edgewidth)
nx.draw_networkx_labels(G,pos,font_size=16)
#plt.show()
plt.savefig("weighted_graph.png") 






##########
#### MDS
##########

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from matplotlib.collections import LineCollection


mds_chart = pd.read_csv('one over lift chart.csv')
mds_chart = mds_chart.drop(mds_chart.columns[0], axis=1) #remove "Unnamed" column, which was original index
mds_chart.index  = mds_chart.columns.values #rename index using car names
#mds_chart.replace(0, np.NaN, inplace=True) #replace diagonals with NaN
#mds_chart.replace(np.NaN, 0, inplace=True) #replace diagonals with 0s
#mds_chart -= mds_chart.mean() #center the data

#similarities = euclidean_distances(mds_chart) #could use euclidean, I'm just using the 1/lift scores themselves
similarities = np.array(mds_chart) #set distances as "similarities", needs to be np.array
#generate mds positions
mds = manifold.MDS(n_components=2, dissimilarity="precomputed", eps=1e-9, random_state=6, n_jobs=1)
pos = mds.fit(similarities).embedding_

fig = plt.figure(figsize=(15,10))
ax = plt.axes([0., 0., 1., 1.])
plt.scatter(pos[:, 0], pos[:, 1], s=50, c='g')

'''
#this adds all the connecting lines

start_idx, end_idx = np.where(pos)
#a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
segments = [[pos[i, :], pos[j, :]]
            for i in range(len(pos)) for j in range(len(pos))]
values = np.abs(similarities)
lc = LineCollection(segments,
                    zorder=0, cmap=plt.cm.hot_r,
                    norm=plt.Normalize(0, values.max()))
lc.set_array(similarities.flatten())
lc.set_linewidths(0.5 * np.ones(len(segments)))
ax.add_collection(lc)
'''
#adding the node labels
for i in range(0,len(mds_chart.columns.values)):
    ax.annotate(mds_chart.columns.values[i], xy=pos[i], size=15)

#plt.show()
plt.savefig("mds_chart.png") 











