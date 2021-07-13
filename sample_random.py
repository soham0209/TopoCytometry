import numpy as np
import os
from seed_pairs import *
import sys

if __name__ == '__main__':
    dir_name = sys.argv[1]
    # dir_name = file_name[0:-4]
    num_samples = 20000
    if len(sys.argv) > 2:
        num_samples = int(float(sys.argv[2]))
    
    cohort_type = 'Healthy_data'
    if 'P' in dir_name:
        cohort_type = 'Patient_data'
    elif 'R' in dir_name:
        cohort_type = 'Recovered_data'
    X = np.loadtxt(os.path.join('Data', cohort_type, dir_name + '.csv'), delimiter=',')
    # protein_indices = [10, 17, 22]
    protein_indices = [10, 17, 22]
    print('Loaded ', dir_name + '.csv')
    X = X[:, protein_indices]
    print('Drawing random samples')
    # num_samples = min(num_samples, X.shape[0])
    sample_indices = np.random.randint(0, X.shape[0], num_samples)
    """
    For now take the first num_samples. Change it later.
    """
    print('Drawing samples')
    X_hat = X[sample_indices[0:num_samples]]
    root_dir = 'recovered_data'
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    tmp_dir_name = os.path.join(root_dir, dir_name)
    if not os.path.exists(tmp_dir_name):
        os.mkdir(tmp_dir_name)
    outfile = tmp_dir_name + '/' + dir_name + '_fvert.txt'
    print('Saving samples', outfile)
    f = open(outfile, 'w')
    f.write(str(3) + '\n')
    np.savetxt(f, X_hat, fmt='%.4f')
    f.close()

