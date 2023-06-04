Step 1: Import necessary libraries 
```py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import warnings 
warnings.simplefilter("ignore")
```
Step 2: Load Dataset
```py
data = pd.read_csv("kaggle/input/genres-v2-spotify/genres_v2.csv") 
data
```
We load the dataset using pandas read_csv, and the data set contains 42305 rows and 22 columns and consists of 18000+ tracks.

Step 3: Exploring the Data
```py
data.iloc[:,:20]
```
We can use the ‘iloc’ method to select the rows and columns that form a data frame by their integer index positions. Example of choosing the first 20 columns of the df.
```
data.info()
```
When you call data.info(), it will print the following information:
- The number of rows and columns in the data frame.
- The name of each column, its data type, and the number of non-null values in that column.
- The total number of non-null values in the data frame.
- The memory usage of the DataFrame.

Step 4: Data Cleaning 
```py
df = data.drop(["type","type","id","uri","track_href","analysis_url","song_name", "Unnamed: 0","title", "duration_ms", "time_signature"], axis =1) 
df
```

Here, we want to clean our data by removing unnecessary columns that add no value to the prediction. We have removed some columns that add no value to this particular problem and put axis = 1, where it drops the columns rather than rows. We are again calling the Data Frame to see the new Data Frame with helpful information.



Step 5: Describe the data

df.describe()


The df.describe( ) method generates descriptive statistics of a Pandas Data Frame. It provides a summary of the central tendency and dispersion and the shape of the distribution of a dataset.
After running this command, you can see all the descriptive statistics of the Data Frame, like std, mean, median, percentile, min, and max.



df["genre"].value_counts()




Step 6: Genre Types

ax = sns.histplot(df["genre"]) 
_ = plt.xticks(rotation=60) 
_ = plt.title("Genres")


axe = sns.histplot(df[“genre”]) generates a histogram of the distribution of values in a Pandas DataFrame named df’s “genre” column. This code may be used to visualize the frequency of some Spotify genres in a music dataset.


Step 7: Drop unnecessary data

df.drop(df.loc[df['genre']=="Pop"].index, inplace=True) 
df = df.reset_index(drop = True) 
df.corr()


The code eliminates or deletes all rows in a Pandas DataFrame where the value in the “genre” column is equal to “Pop”. The DataFrame’s index is then reset to the range where it starts with 0. Lastly, it computes the correlation matrix of the DataFrame’s remaining columns. This code helps study a dataset by deleting unnecessary rows and finding correlations between the remaining variables.



Step 8: Input and Output 

x = df.loc[:,:"tempo"] 
y = df["genre"]


x




y





y.unique()





Step 9: Plot data distribution

k=0 
plt.figure(figsize = (18,14)) 
for i in x.columns: 
  plt.subplot(4,4, k + 1) 
  sns.distplot(x[i]) 
  plt.xlabel(i, fontsize=11) 
  k +=1


The given code generates a grid of distribution plots that allow users to view the distribution of values over several columns in a dataset. Discovering patterns, trends, and outliers in the data by showing the distribution of values in each column. These are helpful and beneficial for exploratory data analysis and finding valuable and potential faults or inaccuracies in a dataset.


Step 10: Split data

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size= 0.2, random_state=42, shuffle = True)
col = xtrain.columns
scalerx = MinMaxScaler()


xtrain = scalerx.fit_transform(xtrain)
xtest = scalerx.transform(xtest)


xtrain = pd.DataFrame(xtrain, columns = col)
xtest = pd.DataFrame(xtest, columns = col)
le = preprocessing.LabelEncoder()
ytrain = le.fit_transform(ytrain)
ytest = le.transform(ytest)


x = pd.concat([xtrain, xtest], axis = 0)
y = pd.concat([pd.DataFrame(ytrain), pd.DataFrame(ytest)], axis = 0)


y_train = le.inverse_transform(ytrain)
y_test = le.inverse_transform(ytest)
y_org = pd.concat([pd.DataFrame(y_train), pd.DataFrame(y_test)], axis = 0)


The code provided preprocesses the data. The first step is to divide the input data into training and testing sets using the Sklearn library’s train test split function. It then adjusts the numerical characteristics in the supplied data using the MinMaxScaler function from the same package. The code encodes the category target variable using the preprocessing module’s LabelEncoder function. As a result, the training and testing sets are preprocessed previously are merged into a single dataset that the machine learning algorithm can process.

Step 11:

early_stopping1 = keras.callbacks.EarlyStopping(monitor = "val_loss", patience = 10, restore_best_weights = True) 
early_stopping2 = keras.callbacks.EarlyStopping(monitor = "val_accuracy", patience = 10, restore_best_weights = True) 

model = keras.Sequential([ 
  keras.layers.Input(name = "input", shape = (xtrain.shape[1])),  
  keras.layers.Dense(256, activation = "relu"),
  keras.layers.BatchNormalization(), keras.layers.Dropout(0.2), 
  keras.layers.Dense(128, activation = "relu"),   
  keras.layers.Dense(128, activation = "relu"), 
  keras.layers.BatchNormalization(), 
  keras.layers.Dropout(0.2), 
  keras.layers.Dense(64, activation = "relu"), 
  keras.layers.Dense(max(ytrain)+1, activation = "softmax") 
]) 
model.summary()


This code creates two early stopping callbacks for model training, one based on validation loss and the other on validation accuracy. Keras’ Sequential API makes a NN model with various connected layers using the ReLU activation function, batch normalization, and dropout regularisation. The summary of the model is printed on the console. The final output layer outputs class probabilities using the softmax activation function. The summary of the model is printed on the console.




Step 12

model.compile(optimizer = keras.optimizers.Adam(), 
             loss = "sparse_categorical_crossentropy", 
             metrics = ["accuracy"])
 
model_history = model.fit(xtrain, ytrain, 
               epochs = 100, 
               verbose = 1, batch_size = 128, 
               validation_data = (xtest, ytest), 
               callbacks = [early_stopping1, early_stopping2])


The following code block uses Keras to compile and train a neural network model. The model is a sequential model with multiple dense layers with relu activation function, batch normalization, and dropout regularisation. “sparse categorical cross entropy” is the loss function utilized. At the same time, “Adam” is the optimizer. The model is trained for 100 epochs, with callbacks that end early based on validation loss and accuracy.



Step 13

print(model.evaluate(xtrain, ytrain)) 
print(model.evaluate(xtest, ytest))


The training data is sent as xtrain and ytrain, whereas the validation data is sent as xtest and ytest. The training history of the model is saved in the model history variable.



Step 14

plt.plot(model_history.history["loss"]) plt.plot(model_history.history["val_loss"]) 
plt.legend(["loss", "validation loss"], loc ="upper right") plt.title("Train and Validation Loss") 
plt.xlabel("epoch") 
plt.ylabel("Sparse Categorical Cross Entropy") 
plt.show()


The following code generates a plot using matplotlib; on the x_axis, we have the epoch, and on the y_axis, we have the sparse Categorical Cross Entropy.


plt.plot(model_history.history["accuracy"]) plt.plot(model_history.history["val_accuracy"]) plt.legend(["accuracy", "validation accuracy"], loc ="upper right") plt.title("Train and Validation Accuracy") 
plt.xlabel("epoch") 
plt.ylabel("Accuracy") 
plt.show()






