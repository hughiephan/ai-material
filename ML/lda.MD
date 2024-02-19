# Linear Discriminant Analysis 

Linear Discriminant Analysis (LDA) works by identifying a linear combination of features that separates or characterizes two or more classes of objects or events. LDA uses class labels in its computation, potentially resulting in improved class differentiation compared to unsupervised methods such as Principal Component Analysis (PCA). The lower-dimensional representation achieved through LDA is more interpretable than the initial feature space. However, LDA is limited in its ability to handle nonlinear relationships since it assumes linear associations between features and classes. If these relationships are nonlinear, LDA may fail to accurately capture the underlying patterns.

![image](https://github.com/hughiephan/DPL/assets/16631121/699a2ca3-5490-43c5-905c-65e412bd805a)

## Step 1: Import libraries
```python
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import roc_curve, auc
from imblearn.over_sampling import RandomOverSampler
```

## Step 2: Dataset

Company Bankruptcy Predction Dataset is from https://www.kaggle.com/datasets/fedesoriano/company-bankruptcy-prediction . This dataset contains financial attributes of companies collected from the Taiwan Economic Journal for the years 1999 to 2009, with bankruptcy status defined based on the business regulations of the Taiwan Stock Exchange. Each entry includes 95 features, with 'Bankrupt?' serving as the class label denoting whether a company went bankrupt. Key attributes include various financial ratios such as Return on Assets (ROA), Gross Margin, Operating Profit Rate, Interest Rates, Tax Rates, Cash Flow, Revenue Per Share, Debt Ratios, Asset Turnover Rates, and various others. These features provide insights into the financial health, performance, and operational efficiency of companies. To decrease the execution time of the SVC model, we will exclusively use the initial 15 features from the dataset and we'll also perform the standard procedure of splitting the dataset into training and test sets.

```python
df = pd.read_csv('../input/company-bankruptcy-prediction/data.csv')
X = df.drop(['Bankrupt?'], axis=1).iloc[:, :15]
y = df['Bankrupt?']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Step 3: Sampling

We use RandomOverSampler for random sampling to balance the number of instances in the bankrupt and non-bankrupt classes within the training set. When using RandomOVerSampler, we use `fit(X, y)` to check inputs and statistics of the sampler and use `fit_resample(X, y)` to actually resample the dataset.

```python
ros = RandomOverSampler()
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
```

## Step 4: Approach 1 (Train with SVC)

We use Support Vector Classifier (SVC) with the parameter `probability=True`, indicating that the classifier will predict probabilities for each class. `probability=True` often go along side with `predict_proba()` to get probability estimates, if we want to get the class label, then we can set `probability=False` and use `predict()`. Next, the classifier is trained using the resampled training data `X_train_resampled` and  `y_train_resampled`. After training, the model predicts the probabilities for the classes of the test set `X_test`. These predicted probabilities are then used to calculate the Receiver Operating Characteristic (ROC) curve. The `y_pred[:, 1]` is used to extract the predicted probabilities of the positive class as ROC only care about the Postive class.

```python
start_time = time.time()
svm = SVC(probability=True)
svm.fit(X_train_resampled, y_train_resampled)
y_pred = svm.predict_proba(X_test)
fpr, tpr, _ = roc_curve(y_test, y_pred[:, 1])
roc_auc = auc(fpr, tpr)
end_time = time.time()
print(end_time - start_time)
```

Total run time of approach 1 should take around 40 seconds

## Step 5: Approach 2 (Train with SVC and LDA)

In LDA, the between-class variance and within-class variance are fundamental components used to determine discriminant functions that effectively separate different classes in a dataset. The between-class variance `m`, assesses the dispersion between the means of distinct classes, highlighting the extent to which class means deviate from one another. Conversely, the within-class variance `S`, gauges the dispersion of data points within individual classes, indicating how tightly clustered or spread out the data is around their respective class means. By optimizing the ratio of between-class variance to within-class variance, LDA identifies the linear combinations of features that maximize class separability, enabling effective dimensionality reduction and classification. In essence, these variance measures serve as critical criteria for LDA to identify the most discriminative features for distinguishing between different classes in the dataset.

![image](https://github.com/hughiephan/DPL/assets/16631121/7c1ed831-d1a2-4422-aeee-51090a2b1e0f)

```python
start_time = time.time()
lda = LinearDiscriminantAnalysis(n_components=1)
X_train_lda = lda.fit_transform(X_train_resampled, y_train_resampled)
X_test_lda = lda.transform(X_test)
svm_with_lda = SVC(probability=True)
svm_with_lda.fit(X_train_lda, y_train_resampled)
y_pred_prob_svm_with_lda = svm_with_lda.predict_proba(X_test_lda)
fpr_svm_with_lda, tpr_svm_with_lda, _ = roc_curve(y_test, y_pred_prob_svm_with_lda[:, 1])
roc_auc_svm_with_lda = auc(fpr_svm_with_lda, tpr_svm_with_lda)
end_time = time.time()
print("Run Time", end_time - start_time)
```

After the you run, we can see that the total time is about 15 seconds

## Step 6: Report
```python
plt.plot(fpr_svm, tpr_svm, label='SVM (AUC = %0.2f)' % roc_auc_svm)
plt.plot(fpr_svm_with_lda, tpr_svm_with_lda, label='SVM with LDA (AUC = %0.2f)' % roc_auc_svm_with_lda)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.show()
```

Due to the curse of dimensionality, SVM with all 15 features resulted in a model that perform poorly. Using all features without any prior selection or dimensionality reduction can lead to longer training times since SVM tends to become computationally expensive with higher dimensions.

![image](https://github.com/hughiephan/DPL/assets/16631121/292d1232-1c03-42bb-a50e-60cf6f6037f4)

## Optional commands:
```
y_train.value_counts() # Calculate the total value of each class 
```

## Reference
- https://www.kaggle.com/code/houcembenmansour/bankruptcy-perdiction-99-67-f1-score
- https://medium.com/aimonks/linear-discriminant-analysis-lda-in-machine-learning-example-concept-and-applications-37f27e7c7e98
- https://machinelearningcoban.com/2017/06/30/lda/
