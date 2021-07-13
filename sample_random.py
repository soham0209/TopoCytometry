import numpy as np
import sys
import os
import argparse
import pandas as pd


def sample(x, outfile):
    num_samples = args.num_kde_samples
    sample_indices = np.random.randint(0, x.shape[0], num_samples)
    print('Drawing samples')
    x_hat = x[sample_indices[0:num_samples]]
    kde_samples = outfile + '_fvert.txt'
    np.savetxt(kde_samples, x_hat, fmt='%.4f')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, required=True, help='Filename to perform kde')
    parser.add_argument('-p', '--proteins', type=int, nargs='+', default=[10, 17, 22], help='Proteins to consider')
    parser.add_argument('-n', '--num_kde_samples', type=int, default=20000, help='Sample from KDE')

    args = parser.parse_args()
    file_name = 'data/' + args.filename
    if '.csv' in file_name:
        file_name = file_name[-4:]
    dir_name = 'KDE_samples/'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    protein_indices = args.proteins
    X = pd.read_csv(file_name + '.csv', sep=',').to_numpy()
    print('Loaded ', file_name + '.csv')
    X = X[:, protein_indices]
    outfilename = os.path.join(dir_name, args.filename)
    sample(X, outfilename)