# dnn_model.py

import numpy as np
import pandas as pd
import csv
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from imblearn.over_sampling import SMOTE, RandomOverSampler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Load dataset
csv_file_path = 'jm1.csv'
X = []
y = []

with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] != 'loc':
            try:
                features = [float(row[i]) for i in range(21)]
                label = 1 if row[21].strip().lower() == 'true' else 0
                X.append(features)
                y.append(label)
            except ValueError:
                continue

X = np.array(X)
y = np.array(y)

print("Original class distribution:", Counter(y))

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Balance classes
try:
    if list(Counter(y).values())[1] > 1:
        smote = SMOTE(random_state=42, k_neighbors=1)
        X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
    else:
        raise ValueError("Too few minority samples.")
except:
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_scaled, y)

print("Resampled class distribution:", Counter(y_resampled))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Build DNN model
model = Sequential()
model.add(Dense(64, input_dim=21, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train
history = model.fit(X_train, y_train, validation_split=0.2, epochs=20, batch_size=32, verbose=1)

# Predict
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype("int32")

# Evaluation
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("Accuracy Score:", accuracy)
print("F1 Score:", f1)

# Compare with Naive Bayes
before = [0.49, 0.66]  # Your NB results
after = [accuracy, f1]

labels = ['Accuracy', 'F1 Score']
x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, before, width, label='Naive Bayes')
plt.bar(x + width/2, after, width, label='DNN')
plt.ylabel('Scores')
plt.title('Model Performance Comparison')
plt.xticks(x, labels)
plt.legend()
plt.tight_layout()
plt.show()
