import numpy as np
from tqdm import tqdm
from scipy.spatial.distance import pdist
from scipy.spatial import cKDTree
import argparse
import gzip
import os


class UnionFind:
    def __init__(self, n):
        self.parent = {}
        self.f = {}
        self.cnt = n

    def make(self, i, val):
        self.parent[i] = i
        self.f[i] = val

    def find(self, x):
        temp = x
        while self.parent[temp] != temp:
            temp = self.parent[temp]
            self.parent[temp] = self.parent[self.parent[temp]]
        return temp

    def union(self, x, y):
        self.parent[y] = x
        self.cnt = self.cnt - 1


def grow_regions(dirname):
    vertex_data = np.loadtxt('KDE_samples/' + dirname + '_fvert.txt')
    # vertex_values = np.loadtxt(dirname + '/' + dirname + '.txt')
    print('Calculating Nearest neighbor distance')
    kdt = cKDTree(vertex_data)
    k = args.nn  # number of nearest neighbors
    dists, neighs = kdt.query(vertex_data, k + 1)
    avg_dists = np.mean(dists[:, 1:], axis=1)
    vertex_values = -avg_dists
    print('Saving vertex values for future use')
    # vertex_data = vertex_data[:, :-1]
    print('Computing edge weights')
    edge_data = pdist(vertex_data)
    print('Edge weights computed ')
    del vertex_data
    num_ver = len(vertex_values)
    uf = UnionFind(num_ver)
    # uf_reg = UnionFind(num_ver)
    max_pers = -float('inf')
    for i, v in enumerate(vertex_values):
        uf.make(i, vertex_values[i])
        # uf_reg.make(i, vertex_values[i])
    print('Sorting edges')
    ind = np.argsort(edge_data)
    print('Computing edge indices')

    p, q = np.triu_indices(num_ver, k=1)
    print('Computing persistence')
    merged_edges = []
    cycle_edges = []
    n = 0
    k = 0
    for i, e_ind in enumerate(tqdm(ind)):
        u, v = p[e_ind], q[e_ind]
        root_v0 = uf.find(u)
        root_v1 = uf.find(v)
        k = k + 1
        if root_v0 == root_v1:
            cycle_edges.append(edge_data[e_ind])
            continue
        f_val = uf.f[root_v1]
        if uf.f[root_v0] > f_val:
            f_val = uf.f[root_v0]
            root_v0, root_v1 = root_v1, root_v0
        elif f_val == uf.f[root_v0]:
            root_v0, root_v1 = min(root_v0, root_v1), max(root_v1, root_v0)
        e_val = edge_data[e_ind]
        pers = e_val - f_val
        max_pers = max(max_pers, pers)
        merged_edges.append([vertex_values[root_v1], e_val])
        n = n + 1
        uf.union(root_v0, root_v1)
        if n == num_ver - 1:
            break
    print('Spanning tree has component ', uf.cnt)
    if k < len(ind):
        cycle_edges = cycle_edges + list(edge_data[ind[k:]])
    del edge_data
    if not os.path.exists('Persistence_Diagrams'):
        os.mkdir('Persistence_Diagrams')
    dim_0_path = 'Persistence_Diagrams/' + dirname + '_dim0.npy.gz'
    dim_0_f = gzip.GzipFile(dim_0_path, 'w')
    np.save(dim_0_f, merged_edges)
    dim_0_f.close()

    del merged_edges

    dim_1_path = 'Persistence_Diagrams/' + dirname + '_dim1.npy.gz'
    dim_1_f = gzip.GzipFile(dim_1_path, 'w')
    np.save(dim_1_f, cycle_edges)
    dim_1_f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, required=True, help='Filename to compute persistence diagram')
    parser.add_argument('-n', '--nn', type=int, default=40, help='Nearest neighbors to consider for assigning '
                                                                 'weight to vertices')
    args = parser.parse_args()
    datafile = args.filename
    grow_regions(datafile)
