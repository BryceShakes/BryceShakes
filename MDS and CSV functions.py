# %%

from time import time
import numpy as np
import pandas as pd
from sklearn import manifold
import matplotlib.pyplot as plt
import os

# %%        my function that should work


# takes the input of an n x n array (symmetrical) with pairwise distances

def Bryce_picture(dist, metric=True):
    if metric == False:
        mds = manifold.MDS(n_components=2,
                       max_iter=100000,
                       n_init = 5,
                       eps=1e-15,
                       metric = False,
                       dissimilarity="precomputed")
        new = mds.fit(dist).embedding_
    elif metric:
        mds = manifold.MDS(n_components=2,
               max_iter=10000,
               n_init = 5,
               eps=1e-3,
               metric = True,
               dissimilarity="precomputed",
               verbose = 1)
        new = mds.fit(dist).embedding_
    plt.scatter(new[:,0], new[:,1])
    plt.show()

def csv_to_mat(path):
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

def bryce_draw_from_raw(path, metric = False):
    arr = csv_to_mat(path)
    Bryce_picture(arr, metric=metric)
    
# %% genus 2 surface

path = r"C:/Users/Bryce/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/bryce/gap-4.11.1/genus_2_vis.csv"

bryce_draw_from_raw(path, True);
    

# %%

#  C:/Users/Bryce/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/bryce/gap-4.11.1
path = r"C:/Users/Bryce/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/bryce/gap-4.11.1/Surface_500.csv"
path2 = r"C:/Users/Bryce/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/bryce/gap-4.11.1/free_vis_mat_noid.csv" 


a1 = csv_to_mat(path)
a2 = csv_to_mat(path2)

Bryce_picture(a1, metric = True)
Bryce_picture(a2, metric = True)

#bryce_draw_from_raw(path)


# %% testing speeds

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
           dissimilarity = "precomputed")
    new = mds.fit(a1).embedding_
    plt.scatter(new[:,0], new[:,1])
    plt.title(str(i))
    plt.show()
    time_arr.append([i,time() - now - sum([x[1] for x in time_arr])])
    
    