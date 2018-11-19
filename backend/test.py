import pandas as pd
import numpy as np
import tflearn
from tflearn.data_utils import load_csv
from tflearn.datasets import titanic
from sklearn.model_selection import train_test_split
import sys

# Download the Titanic dataset
titanic.download_dataset('titanic_dataset.csv')

# Load CSV file, indicate that the first column represents labels
data, labels = load_csv('titanic_dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)

# Make a df out of it for convenience
df = pd.DataFrame(data)

# Do a test / train split
X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.33, random_state=42)

def preprocess(r):
    r = r.drop([1], axis=1,errors='ignore')
    r[2] = r[2].astype('category')
    r[2] = r[2].cat.codes
    r[6] = r[6].astype('category')
    r[6] = r[6].cat.codes
    for column in r.columns:
        r[column] = r[column].astype(np.float32)
    return r.values

X_train = preprocess(X_train)
pd.DataFrame(X_train).head()

X_train.shape
y_train.shape

#Reset the graph first
import tensorflow as tf
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, 7])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
print(X_train)
sys.exit()
# Start training (apply gradient descent algorithm)
#model.fit(X_train, y_train, n_epoch=20, batch_size=32, show_metric=True)
# With cross validation
#model2 = tflearn.DNN(net)
model2.fit(X_train, y_train, n_epoch=20, batch_size=32, show_metric=True, validation_set=0.1)

X_test = preprocess(X_test)
metric_train = model.evaluate(X_train, y_train)
metric_test = model.evaluate(X_test, y_test)
metric_train_1 = model2.evaluate(X_train, y_train)
metric_test_1 = model2.evaluate(X_test, y_test)

print('Model 1 Accuracy on train set: %.9f' % metric_train[0])
print("Model 1 Accuracy on test set: %.9f" % metric_test[0])
print('Model 2 Accuracy on train set: %.9f' % metric_train_1[0])
print("Model 2 Accuracy on test set: %.9f" % metric_test_1[0])

# Let's create some data for DiCaprio and Winslet
dicaprio = [3, 'Jack Dawson', 'male', 19, 0, 0, 'N/A', 5.0000]
winslet = [1, 'Rose DeWitt Bukater', 'female', 17, 1, 2, 'N/A', 100.0000]
# Preprocess data
dicaprio, winslet = preprocess(pd.DataFrame([dicaprio, winslet]))
# Predict surviving chances (class 1 results)
pred = model.predict([dicaprio, winslet])
print("DiCaprio Surviving Rate:", pred[0][1])
print("Winslet Surviving Rate:", pred[1][1])