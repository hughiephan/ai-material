# Linear Discriminant Analysis 

![image](https://github.com/hughiephan/DPL/assets/16631121/f2360acb-3f2a-45d2-a328-4c69bbcc42af)

## Step 1: Import libraries
```python
import numpy as np
import pandas as pd
import seaborn as sns 
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
X = df.drop(['Bankrupt?'], axis=1)
y = df['Bankrupt?']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

## Step 3: Sampling
```python
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
```

## Step 4: Train with SVC
```python
start_time = time.time()
svm_without_lda = SVC(kernel='linear', probability=True)  # Enable probability estimation
svm_without_lda.fit(X_train_resampled, y_train_resampled)
y_pred_prob_svm_without_lda = svm_without_lda.predict_proba(X_test)
fpr_svm_without_lda, tpr_svm_without_lda, _ = roc_curve(y_test, y_pred_prob_svm_without_lda[:, 1])
roc_auc_svm_without_lda = auc(fpr_svm_without_lda, tpr_svm_without_lda)
end_time = time.time()
print("Time", end_time - start_time)
```

## Step 5: Train with SVC and LDA
```python
start_time = time.time()
n_components = min(X_train_resampled.shape[1], len(np.unique(y_train_resampled)) - 1)  # Ensure within limit
lda = LinearDiscriminantAnalysis(n_components=n_components)
X_train_lda = lda.fit_transform(X_train_resampled, y_train_resampled)
X_test_lda = lda.transform(X_test)
svm_with_lda = SVC(kernel='linear', probability=True)  # Enable probability estimation
svm_with_lda.fit(X_train_lda, y_train_resampled)
y_pred_prob_svm_with_lda = svm_with_lda.predict_proba(X_test_lda)
fpr_svm_with_lda, tpr_svm_with_lda, _ = roc_curve(y_test, y_pred_prob_svm_with_lda[:, 1])
roc_auc_svm_with_lda = auc(fpr_svm_with_lda, tpr_svm_with_lda)
end_time = time.time()
print("Time", end_time - start_time)
```

## Step 6: Report
```python
plt.figure(figsize=(8, 6))
plt.plot(fpr_svm_without_lda, tpr_svm_without_lda, color='blue', lw=2, label='SVM without LDA (AUC = %0.2f)' % roc_auc_svm_without_lda)
plt.plot(fpr_svm_with_lda, tpr_svm_with_lda, color='red', lw=2, label='SVM with LDA (AUC = %0.2f)' % roc_auc_svm_with_lda)
plt.plot([0, 1], [0, 1], color='black', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()
```

## Reference
- https://www.kaggle.com/code/houcembenmansour/bankruptcy-perdiction-99-67-f1-score
