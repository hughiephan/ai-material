# Linear Discriminant Analysis 

![Untitled-2023-07-31-0913](https://github.com/hughiephan/DPL/assets/16631121/f2a56402-2264-49f8-bff6-93c6e2855b56)

Linear Discriminant Analysis (LDA) utilizes class labels in its computation, potentially resulting in improved class differentiation compared to unsupervised methods such as Principal Component Analysis (PCA). The lower-dimensional representation achieved through LDA is more interpretable than the initial feature space. However, LDA is limited in its ability to handle nonlinear relationships since it assumes linear associations between features and classes. If these relationships are nonlinear, LDA may fail to accurately capture the underlying patterns.

![image](https://github.com/hughiephan/DPL/assets/16631121/6c2f547c-2c6a-4b3e-aeec-e8c7b7a348c3)

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
```python
df = pd.read_csv('../input/company-bankruptcy-prediction/data.csv')
X = df.drop(['Bankrupt?'], axis=1).iloc[:, :15]
y = df['Bankrupt?']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Step 3: Sampling
```python
ros = RandomOverSampler()
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
```

## Step 4: Train with SVC
```python
start_time = time.time()
svm = SVC(probability=True)
svm.fit(X_train_resampled, y_train_resampled)
y_pred_prob_svm = svm.predict_proba(X_test)
fpr_svm, tpr_svm, _ = roc_curve(y_test, y_pred_prob_svm[:, 1])
roc_auc_svm = auc(fpr_svm, tpr_svm)
end_time = time.time()
print("Time", end_time - start_time)
```

Should take around: 40 seconds

## Step 5: Train with SVC and LDA

After the you run, we can see that the total time is about 15 seconds

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

## Reference
- https://www.kaggle.com/code/houcembenmansour/bankruptcy-perdiction-99-67-f1-score
- https://medium.com/aimonks/linear-discriminant-analysis-lda-in-machine-learning-example-concept-and-applications-37f27e7c7e98
- https://machinelearningcoban.com/2017/06/30/lda/
