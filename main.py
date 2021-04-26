import numpy as np
from xgboost import XGBClassifier
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from matplotlib import pyplot
from xgboost import plot_importance
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn.metrics import accuracy_score


# load data

def classify(num_folds, feature_names):
    healthy_data = np.load('healthy_data.npy')
    patient_data = np.load('patient_data.npy')
    dataset = np.concatenate((healthy_data, patient_data))
    ind = np.random.permutation(dataset.shape[0])
    X = dataset
    Y = np.zeros((dataset.shape[0],))
    Y[0:int(dataset.shape[0] / 2)] = 1
    X = X[ind]
    Y = Y[ind]
    print('Dataset shape:', X.shape)
    print('Labels shape:', Y.shape)
    print('Healthy:', healthy_data.shape[0], 'Patient:', patient_data.shape[0])

    seed = 0
    rng = np.random.RandomState(seed)
    X = pd.DataFrame(X, columns=feature_names)
    kf = KFold(n_splits=num_folds, shuffle=True, random_state=rng)

    xgb_model = XGBClassifier()

    epoch = 0
    for train_index, test_index in kf.split(X):
        epoch += 1
        xgb_model.fit(X.iloc[train_index], Y[train_index])
        y_pred = xgb_model.predict(X.iloc[test_index])
        y_true = Y[test_index]
        # predictions = [round(value) for value in y_pred]
        report = accuracy_score(y_true, y_pred)
        print('Fold: {:2d} Acc: {:.5f}'.format(epoch, report))
    xgb_model.feature_names = feature_names
    ax = plot_importance(xgb_model)
    ax.figure.savefig('feature_importance.png')


if __name__ == '__main__':
    num_kf = int(sys.argv[1])
    features = ["CD45RA", "PD-1", "IgD", "CXCR5", "CD8", "CD19", "CD3", "Tox", "CD16", "CD138", "Eomes", "TCF-1",
                "CD38", "CD95", "ICOS", "CCR7", "CD21", "Ki-67", "CD27", "CD4", "CX3CR1", "CD39", "T-bet",
                "HLA-DR", "CD20"]
    classify(num_kf, features)
