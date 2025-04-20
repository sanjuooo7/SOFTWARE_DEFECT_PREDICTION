import pandas as pd
import numpy as np
from matplotlib.pyplot import figure, bar, ylabel, tight_layout, legend, xticks, show, title, ylim
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE, RandomOverSampler
from collections import Counter
import csv

# Load dataset from CSV
csv_file_path = 'jm1.csv'  # Update path if needed

X = []
y = []

# Read and process CSV rows
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
                continue  # Skip rows with invalid data

X = np.array(X)
y = np.array(y)

print("Original class distribution:", Counter(y))

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Handle class imbalance
try:
    if list(Counter(y).values())[1] > 1:
        smote = SMOTE(random_state=42, k_neighbors=1)
        X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
    else:
        raise ValueError("Too few minority samples for SMOTE. Switching to RandomOverSampler.")
except:
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_scaled, y)

print("Resampled class distribution:", Counter(y_resampled))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# Train Naive Bayes classifier
model = GaussianNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
conf_matrix = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", conf_matrix)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Performance Metrics
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy Score: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")

# Baseline comparison (update these based on previous results)
baseline_accuracy = 0.49  # Replace with your old accuracy
baseline_f1 = 0.33        # Replace with your old F1 score

# Data for visualization
before = [baseline_accuracy, baseline_f1]
after = [accuracy, f1]

labels = ['Accuracy', 'F1 Score']
x = np.arange(len(labels))
width = 0.35

# Plotting
figure(figsize=(8, 5))
bar(x - width / 2, before, width, label='Before', color='lightcoral')
bar(x + width / 2, after, width, label='After', color='mediumseagreen')
ylabel('Score')
ylim(0, 1)
title('Model Performance Comparison')
xticks(x, labels)
legend()
tight_layout()
show()
