from gudhi.hera.wasserstein import wasserstein_distance
from scipy.stats import wasserstein_distance as wa
import numpy as np
import gzip
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, nargs=2, required=True, help='Filename to compute persistence diagram')
    args = parser.parse_args()
    dim = 0
    f1_name = 'Persistence_Diagrams/' + args[0] + '_dim' + str(dim) + '.npy.gz'
    f1 = gzip.GzipFile(f1_name, "r")
    arr_1 = np.load(f1)
    print(f1_name, 'loaded')
    f2_name = 'Persistence_Diagrams/' + args[1] + '_dim' + str(dim) + '.npy.gz'
    f2 = gzip.GzipFile(f2_name, "r")
    arr_2 = np.load(f2)
    print(f2_name, 'loaded')

    print('Computing wasserstein dist for dim:', dim)
    dist = wasserstein_distance(arr_1, arr_2)
    print('Wasserstein distance for dim {:d}: {}'.format(dim, dist))

    del arr_1
    del arr_2

    dim = 1
    f1_name = 'Persistence_Diagrams/' + args[0] + '_dim' + str(dim) + '.npy.gz'
    f1 = gzip.GzipFile(f1_name, "r")
    arr_1 = np.load(f1)
    print(f1_name, 'loaded')
    f2_name = 'Persistence_Diagrams/' + args[1] + '_dim' + str(dim) + '.npy.gz'
    f2 = gzip.GzipFile(f2_name, "r")
    arr_2 = np.load(f2)
    print(f2_name, 'loaded')

    print('Computing wasserstein dist for dim:', dim)
    dist = wa(arr_1, arr_2)
    print('Wasserstein distance for dim {:d}: {}'.format(dim, dist))


