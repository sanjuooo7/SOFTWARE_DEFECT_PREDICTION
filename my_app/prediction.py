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
                X.append(r)
                if row[21]=="true":
                 y.append(1)
                else:
                 y.append(0)
            except:
                pass

# Generate a sample imbalanced dataset (you can replace this with your dataset)
# X, y = make_classification(n_classes=2, class_sep=2, weights=[0.1, 0.9],
#                            n_informative=3, n_redundant=1, flip_y=0,
#                            n_features=20, n_clusters_per_class=1,
#                            n_samples=1000, random_state=42)

# Split the dataset into training and testing sets

# Display class distribution before applying SMOTE
print("Class distribution before SMOTE:")
print(pd.Series(y).value_counts())

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_train_resampled, y_train_resampled, test_size=0.2, random_state=42)


# Display class distribution after applying SMOTE
print("\nClass distribution after SMOTE:")
print(pd.Series(y_train_resampled).value_counts())
#
# # Train a classifier on the balanced dataset
# clf = RandomForestClassifier(random_state=42)
# # clf.fit(X_train_resampled, y_train_resampled)
# clf.fit(X_train, y_train)
#
# # Make predictions on the test set
# y_pred = clf.predict(X_test)
#
# # Display classification report
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))


import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Generate synthetic time series data
np.random.seed(42)
data = np.random.randn(100, 1)

# Function to create sequences for time series data
def create_sequences(data, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        sequence = data[i : i + sequence_length]
        target = data[i + sequence_length]
        sequences.append((sequence, target))
    return np.array(sequences)

# Create sequences with a sequence length of 10
sequence_length = 10
sequences = create_sequences(data, sequence_length)

# Split data into training and testing sets


# Convert data to numpy arrays
X_train, y_train =np.array(X_train)[:-1], np.array(y_train)[:, -1]
X_test, y_test = np.array(X_test)[:, :-1], np.array(y_test)[:, -1]

# Reshape data for LSTM input (samples, time steps, features)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length - 1, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model on test data
mse = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Data: {mse}')

# Make predictions on test data
predictions = model.predict(X_test)

# Display actual vs predicted values
for i in range(len(predictions)):
    print(f"Actual: {y_test[i]}, Predicted: {predictions[i][0]}")
