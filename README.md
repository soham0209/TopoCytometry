# TopoCytometry
This repository contains code for the paper titled "etermining clinically relevant features in cytometry data using persistent homology" authored by Soham Mukherjee, Darren Wethington, Tamal K. Dey, Jayajit Das.

### Requirements:
These packages are used in the files:
numpy~=1.19.2  
pandas~=1.1.3  
scikit-learn~=0.23.2  
matplotlib~=2.2.2  
gudhi~=3.4.1  
scipy~=1.5.2  
tqdm~=4.54.1  
xgboost 


You can install these files by doing:
python -m pip install -r requirements.txt

Please use Python 3 to run this code.

## Step 1: Relevant protein selection
**Important:** To run this, please place all your files inside 'data' folder in '.csv' format. Example file format is given in the data directory. Now list all the healthy and patients in files.txt file inside the 'data' directory. There is an example 'files.txt' in the 'data' folder. Note you can comment files with '#' symbol.

The 'files.txt' file has the following format:

---
Healthy:

h1.csv

h2.csv

\#h3.csv  '#' to comment out

Patient:


p1.csv

p2.csv

---
python get_important_features.py --fold number\_of\_folds\_in cross\_validation(default is 5)

This will generate a diagram in the main directory called feature_importance.png. This gives an ordering of proteins.

## Step 2: Kernel Density Estimation sampling

python --filename h1 --proteins 0 1 2 --num\_kde\_samples 20000


If your original filename is h1.csv, please pass h1 to --filename flag.  The protein flag is **important**. These indices correspond to columns of proteins in the 'h1.csv' file. **Notice** that indices are 0-based. This will create a directory named KDE\_samples and generate a file named h1_fvert.txt inside KDE\_samples directory.


## Step 3: Persistence diagram and Wasserstein distance:
### Computing persistence diagrams
python compute_persistence.py -f h1 -n 40


This commands compute persistence diagram by building a complete graph on the KDE sampled data of h1.csv [stored as KDE\_samples\h1_fvert.txt] as described in the paper. The -n flag controls nearest neighbors to consider for computing vertex weights. This creates a directory named 'Persistence\_Diagrams' and two files h1\_dim0.npy.gz and h1_\dim1.npy.gz. The first file contains (b, d) pairs for vertices and the second one contains birth values of the 1-dim homology classes. For more details please refer to the paper and the source code.
### Computing Wasserstein Distances
python compute_wasser.py -f h1 p1 

This command prints the Wasserstein distance between persistence diagrams of h1 and p1 [both 0 and 1 dim PD].

## Example:
- python get_important_features.py --fold 5
- python sample\_kde.py --filename HD2020_007 --proteins 10 17 22  --num_kde_samples 20000

 [It takes Eomes,T-Bet, Ki-67 proteins since index of Eomes is 10 in HD2020_007.csv file]
- python compute_persistence -f HD2020_007 -n 40
- python  compute_wasser.py -f HD2020_007 HD2020_016


**Note:** You need to sample and generate persistence diagram of both before computing Wasserstein distance between HD2020_007 and HD2020_016.

![Persistence diagram shows difference between healthy control and persons infected with COVID-19](panel_figs.svg)