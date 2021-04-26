//
// Created by Soham Mukherjee on 9/13/20.
//
#include <iostream>
#include <fstream>
#include <string>
#include "PointSet.h"
#include <ANN/ANN.h>					// ANN declarations
#include <ANN/ANNx.h>					// more ANN declarations
#include <ANN/ANNperf.h>				// performance evaluation
#define ZERO 1e-10

int main(int argc, char* argv[]) {
    std::string dir_name = argv[1];
    std::string point_file = dir_name + "/" + dir_name + "_fvert.txt";
    int num_nbrs = std::stoi(argv[2]);


    PointSet ptSet;
    ptSet.ReadPointsFromFile(point_file.c_str());
    int nPts = (int) ptSet._PointSet->size();
    // Last column is not coordinate but filtration value
    int dim = ptSet._dimension;

    std::vector<float> dist(nPts, 0.0);

    ANNpoint queryPt;
    ANNidxArray nnIdx = nullptr;
    ANNdistArray dists = nullptr;

    queryPt = annAllocPt(dim); // need to delloc

    nnIdx = new ANNidx[nPts];
    dists = new ANNdist[nPts];
    /**************************/

    ANNpointArray dataPts;
    dataPts = annAllocPts(nPts, dim);
    // adding vertices


    for (int i = 0; i < nPts; i++) {
        for (int j = 0; j < dim; j++) {
            dataPts[i][j] = (*ptSet._PointSet)[i][j];
        }
    }
    ///////////////////
    ANNkd_tree *kdTree;
    kdTree = new ANNkd_tree(dataPts,
                            nPts,
                            dim);
    //boost::progress_display disp(nPts);
    for (auto i = 0; i < nPts; i++) {
        //++disp;
        for (int j = 0; j < dim; j++) {
            queryPt[j] = (*ptSet._PointSet)[i][j];
        }
        kdTree->annkSearch(dataPts[i], num_nbrs, nnIdx, dists, 0.01);
        for (auto j = 0; j < num_nbrs; j++) {
            dist[i] = dist[i] + dists[j];
        }
        dist[i] = sqrt(dist[i]) / (float)num_nbrs;
    }

    delete[] nnIdx;
    delete[] dists;
    delete kdTree;
    if (dataPts)
        annDeallocPts(dataPts);
    if (queryPt)
        annDeallocPt(queryPt);
    std::cout << "Writing vertex weights" << std::endl;
    std::string weight_file_path = dir_name + "/" + dir_name + ".txt";
    std::ofstream weight_file(weight_file_path);
    for(auto &v:dist){
        weight_file << v << std::endl;
    }
    weight_file.close();
}
