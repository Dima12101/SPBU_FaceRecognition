import numpy as np

def dist(arr1, arr2):
    return np.sqrt(np.sum((arr1 - arr2)**2))
