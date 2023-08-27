# Predict Melbourne House Price

## Dataset
https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot

## Step: Import Libraries
```R
library(tidyverse) # utility functions
library(rpart) # for regression trees
library(randomForest) # for random forests
```

## Step: Import Data
```R
melbourne_data <- read_csv("/kaggle/input/melbourne-housing-snapshot/melb_data.csv", show_col_types = FALSE)
```

## Step: Train our model
```R
fit <- rpart(Price ~ Rooms + Bathroom + Landsize + BuildingArea + YearBuilt + Lattitude + Longtitude, data = melbourne_data)
```

## Step: Show the predictions
```R
plot(fit, uniform=TRUE)
text(fit, cex=.6)
```

## Step: Make prediction
```R
print("Our prediction")
predict(fit, melbourne_data[1,])
print("Actual Price")
melbourne_data[1,]$Price
```

![image](https://github.com/hughiephan/DPL/assets/16631121/ea1c695c-97aa-490a-a6dc-0b53bec05079)

## References
- Kaggle Notebook by Rachel Tatman (Welcome to Data Science in R)
