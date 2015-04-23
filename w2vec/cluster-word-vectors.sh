#!/bin/sh

C="300"
I="50"

./kmeans -input vectors.txt -output word-clusters.txt -nclasses $C -niter $I
