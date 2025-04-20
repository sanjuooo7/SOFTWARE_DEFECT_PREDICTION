
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import Session
import os
import librosa
import warnings
from keras.models import Sequential
from keras.layers import Dense
import numpy
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np
config = ConfigProto()
config.gpu_options.allow_growth = True
sess = Session(config=config)

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import csv

# Specify the path to your CSV file
csv_file_path = 'jm1.csv'
# csv_file_path = r'C:\Users\hp\PycharmProjects\myproject\my_app\jm1.csv'
# Open the CSV file

X=[]
y=[]
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        if row[0]!='loc':
            try:
                print(row)
                r=[]
                for i in range(0,21):
                    r.append(float(row[i]))
                X.append(list(r))
                if row[21]=="true":
                 y.append(1)
                else:
                 y.append(0)
            except:
                pass



smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X, y)

# X_train, X_test, y_train, y_test = train_test_split(X_train_resampled, y_train_resampled, test_size=0.2, random_state=42)


X=np.array(X_train_resampled)
Y=y_train_resampled


model = Sequential()
model.add(Dense(12, input_dim=21, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
history = model.fit(X, Y, validation_split=0.20, epochs=20, batch_size=10, verbose=0)
print (history)

yyy=[X[90]]
yyy=numpy.array(yyy)

res=model.predict_classes(yyy,batch_size=1, verbose=0)
# print(outputlabels[int(res[0])-1])
# print(history.history.keys())
#
print('Accuracy')
print(history.history['accuracy'])
trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.20, random_state=4)
res=model.predict_classes(testX,batch_size=1,verbose=0)
print(testY)

res1=[]
for r in res :
    res1.append(r[0])
print(res1)
cm=confusion_matrix(testY,res1)
print("confusion_matrix")
print(cm)