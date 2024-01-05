# %%

# libraries
from time import time
import numpy as np
import pandas as pd
from sklearn import manifold
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import os

# %%

# This may cause issues, only run it if you have a qt5 toolkit 
# allows for plots to be interacted with, remove hashtag and run
# %matplotlib qt


# %%        my function that should work


# takes the input of an n x n array (symmetrical) with pairwise distances, called a distance or dissimilarity matrix
# performs MDS, either metric or non based on input, with fixed (although tuned) parameters
# returns the points as cartesian co-ords of specified dimension in Euclidean space
# also plots the graph if dimensions = 2
def plot_from_matrix(D, metric=True, title = None, dimensions = 2):
    if metric == False:
        mds = manifold.MDS(n_components=dimensions,
                       max_iter=100000,
                       n_init = 5,
                       eps=1e-3,
                       metric = False,
                       dissimilarity="precomputed")
        new = mds.fit(D).embedding_
    elif metric:
        mds = manifold.MDS(n_components=dimensions,
               max_iter=10000,
               n_init = 5,
               eps=1e-3,
               metric = True,
               dissimilarity="precomputed")
        new = mds.fit(D).embedding_
    if dimensions == 2:
        plt.figure(figsize=(12.80,7.20))
        plt.scatter(new[:,0], new[:,1])
        if title != None:
            plt.title(title)
        plt.xticks([])
        plt.yticks([])
        plt.show()
    elif dimensions == 3:
        fig = plt.figure(figsize=(19.20,10.80))
        ax = fig.add_subplot(projection='3d')
        ax.scatter(new[:,0], new[:,1], new[:,2])
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.zaxis.set_ticklabels([])
        if title != None:
            plt.title(title)
        plt.show()
    return new

# takes the CSV output from distance-matrix-generation-functions.g and converts into a numpy array
# accepts a csv where the record printed is any from 'GetVisualMatrixRec', 'MatToRec2', 'MatToRec' or direct result of PrintMatrix
def csv_to_matrix(path):
    assert os.path.isfile(path)
    df = pd.read_csv(path)
    if df.shape[1] > 1:
        arr = []
        for i in range(df.shape[1]):
            arr.append(eval(df.iloc[0,i]))
        arr = np.array(arr)
    elif df.shape[1] == 1:
        arr = np.array(eval(df.iloc[0,0]))
    return arr

# combines plot_from_matrix and csv_to_matrix. 
# supply with path as location of CSV file from GAP and equal parameters to 
def plot_from_csv(path, metric = True, title = None,  dimensions =2 ):
    arr = csv_to_matrix(path)
    return plot_from_matrix(arr, metric=metric, title=title, dimensions = dimensions)


# not my code, edited slightly to nest in function from https://stackoverflow.com/questions/54055761/checking-triangle-inequality-in-a-massive-numpy-matrix
def check_triangle_ineq(D):
    for i in range(len(D)):
        for j in range(i):
            if not all(D[i,j] <= D[i,:] + D[:,j]):
                return False
    return True

# count the number of triangles in of D that violate the traingle inequality. from a total of NC3, where D is an NxN matrix
# again not my code, was altered from the check_triangle_ineq to count exceptions
def measure_triangle_ineq(D):
    N = len(D)
    test = 0
    for i in range(N):
        for j in range(i):
            test += sum(D[i,j] > D[i,:] + D[:,j])
    return test

# %% testing speeds and tuning manifold params
path = r"--Path to dissimilarity matrix of free group was here--"
a1 = csv_to_matrix(path)

testing = [
    [False, 1e-15, 100000],
    [False, 1e-9, 100000],
    [False, 1e-15, 1000],
    [False, 1e-9, 1000],
    [True, 1e-15, 100000],
    [True, 1e-9, 100000],
    [True, 1e-3, 100000],
    [True, 1e-15, 10000],
    [True, 1e-9, 10000],
    [True, 1e-3, 10000],
    [True, 1e-15, 1000],
    [True, 1e-9, 1000],
    [True, 1e-3, 1000],
    ]

now = time()
time_arr = []
for i in testing :
    mds = manifold.MDS(n_components=2,
           max_iter = i[2],
           n_init = 5,
           eps = i[1],
           metric = i[0],
           n_jobs = 6,
           dissimilarity = "precomputed")
    new = mds.fit(a1).embedding_
    plt.scatter(new[:,0], new[:,1])
    plt.title(str(i))
    plt.show()
    time_arr.append([i,time() - now - sum([x[1] for x in time_arr])])
    
# %% testing with some groups


list1 = ["strebel", "bryce", "dihedral", "z3"]


for i in list1:
    path = r"--INSERT FOLDER PATH HERE--"+i+".csv"
    mat = csv_to_matrix(path)
    print(check_triangle_ineq(mat))
    plot_from_matrix(mat, True, title = i+'2d')
    plot_from_matrix(mat, True, title = i+'3d', dimensions = 3)
    #plot_from_matrix(path, False, title = i+'non-metric')



#%% getting numbers for points in sphere of free group.

import decimal

a = decimal.Decimal(4*3**999)
format(a, '.2e')

b = decimal.Decimal(1e+120)
c = decimal.Decimal((1000*8*4*3**999) /b )
format(c, '.2e')



# %% 3-D to 2-D plot

points = pd.DataFrame(columns=['x','y','z'])

for i in range(1000):
    coords = np.array([])
    # generate 4 gaus points
    for j in range(3):
        coords =  np.append(coords, np.random.normal())
    # normalise to fit on unit sphere
    coords = coords/(np.sum(coords**2)**0.5)
    # add to df
    points.loc[i] = coords
    

fig = plt.figure(figsize=(19.20,10.80))
ax = fig.add_subplot(projection='3d')
ax.scatter(points['x'], points['y'], points['z'], color = 'r')
plt.show()

points_arr = points.to_numpy()
dist_mat = euclidean_distances(points_arr, points_arr)

mds_3d = manifold.MDS(n_components=2,
       max_iter=10000,
       n_init = 5,
       eps=1e-3,
       metric = True,
       dissimilarity="precomputed")
new = mds_3d.fit(dist_mat).embedding_

plt.figure(figsize=(12.80,7.20))
plt.scatter(new[:,0], new[:,1], color ='r')
plt.show()