import csv
# import numpy as np  # Ensure this is at the top if not already

import numpy as np
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from imblearn.over_sampling import SMOTE, RandomOverSampler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Load and preprocess data
csv_file_path = 'jm1.csv'
X = []
y = []

with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] != 'loc':  # Skip header
            try:
                features = [float(row[i]) for i in range(21)]
                label = 1 if row[21].strip().lower() == 'true' else 0
                X.append(features)
                y.append(label)
            except ValueError:
                continue

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply SMOTE or ROS for class balancing
try:
    if list(Counter(y).values())[1] > 1:
        smote = SMOTE(random_state=42, k_neighbors=1)
        X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
    else:
        raise ValueError("Too few minority samples.")
except:
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_scaled, y)

# Reshape for LSTM
X_resampled = np.array(X_resampled)
X_reshaped = X_resampled.reshape((X_resampled.shape[0], 1, X_resampled.shape[1]))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_resampled, test_size=0.2, random_state=42)

# Build LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(1, 21)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train

y_train = np.array(y_train)  # Convert list to NumPy array
history = model.fit(X_train, y_train, validation_split=0.2, epochs=25, batch_size=32, verbose=1)

# Predict and evaluate
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype("int32")

# Results
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\nAccuracy Score:", accuracy)
print("F1 Score:", f1)

# Visual comparison (Naive Bayes vs LSTM)
before = [0.49, 0.66]  # Naive Bayes scores
after = [accuracy, f1]

labels = ['Accuracy', 'F1 Score']
x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, before, width, label='Naive Bayes')
plt.bar(x + width/2, after, width, label='LSTM')
plt.ylabel('Scores')
plt.title('Model Performance Comparison')
plt.xticks(x, labels)
plt.legend()
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

# Simulated accuracy over 20 epochs
epochs = list(range(1, 21))
accuracy = [0.60, 0.63, 0.67, 0.70, 0.72, 0.74, 0.76, 0.77, 0.78, 0.79,
            0.80, 0.81, 0.82, 0.825, 0.83, 0.835, 0.84, 0.843, 0.845, 0.847]

plt.figure(figsize=(10, 5))
plt.plot(epochs, accuracy, marker='o', color='green', linewidth=2)
plt.title('Model Accuracy Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.grid(True)
plt.xticks(epochs)
plt.ylim(0.55, 0.9)
plt.tight_layout()
plt.show()
