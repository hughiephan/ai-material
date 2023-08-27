# K-Means Clustering

## Dataset
https://www.kaggle.com/datasets/akram24/wine-pca

## Step: Import libraries
```R
library(tidyverse)
library(GGally)
```

## Step: Import Data
```R
wines <- read.csv("/kaggle/input/wine-pca/Wine.csv")
wines <- wines[, -14]
```

## Step: Run and visualzie K3
```R
winesNorm <- as.data.frame(scale(wines))
wines_k3 <- kmeans(winesNorm, centers=3)
```

## Step: Visualize k3
```R
ggpairs(cbind(wines, Cluster=as.factor(wines_k3$cluster)),
        columns=1:3, aes(colour=Cluster),
        lower=list(continuous="points"),
        upper=list(continuous="blank"),
        axisLabels="none")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/69a07cd4-ae50-4cde-8438-c16bee74952b)

## References
- Kaggle Notebook by Rachel Tatman (Welcome to Data Science in R)
