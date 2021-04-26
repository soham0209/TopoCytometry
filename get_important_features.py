import numpy as np
from main import classify
import argparse
import pandas as pd

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fold', type=int, default=5, help='Number of folds in cross validation')

	args = parser.parse_args()
	with open('data/files.txt', 'r') as f:
		healthy_file_names = []
		patient_file_names = []
		file_names = []
		for line in f:
			if '#' in line:
				continue
			elif 'healthy:' in line or 'Healthy:' in line:
				file_names = healthy_file_names
				continue
			elif 'patient:' in line or 'Patient:' in line:
				file_names = patient_file_names
				continue
			file_names.append(line.strip('\n'))
	print('Healthy controls:', healthy_file_names)
	print('Infected patients:', patient_file_names)
	print('Preparing training data')
	healthy_files = []
	patient_files = []
	print('Reading healthy control data...')
	column_names = []
	for file in healthy_file_names:
		ext = file[-3:]
		data = None
		if ext == 'txt':
			data = np.loadtxt('data/' + file)
		elif ext == 'csv':
			df = pd.read_csv('data/' + file)
			column_names = df.columns
			data = df.to_numpy()
		else:
			print('Currently txt and csv is supported only')
		healthy_files.append(data)
	print('Saving healthy control data')
	healthy_data = np.vstack(healthy_files)
	np.save('healthy_data.npy', healthy_data)
	del healthy_files
	del healthy_data

	print('Reading infected patients data...')
	for file in patient_file_names:
		ext = file[-3:]
		data = None
		if ext == 'txt':
			data = np.loadtxt('data/' + file)
		elif ext == 'csv':
			df = pd.read_csv('data/' + file)
			column_names = df.columns
			data = df.to_numpy()
		else:
			print('Currently txt and csv is supported only')
		patient_files.append(data)
	print('Saving infected patients data')
	patient_data = np.vstack(patient_files)
	np.save('patient_data.npy', patient_data)
	del patient_files
	del patient_data
	classify(args.fold, column_names)
