import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import matplotlib.pyplot as plt
import os

# --- 1. Data Loading and Preprocessing ---
# load dataset from csv file 
data = pd.read_csv('../Data/ecoli.data', sep='\s+', header=None, engine='python') 
data.head()

le = preprocessing.LabelEncoder()
for column_name in data.columns:
    if data[column_name].dtype == object:
        data[column_name] = le.fit_transform(data[column_name])
    else:
        pass

n = len(data.columns) 
y = data.iloc[:,-1] 
X = data.iloc[:, 0:n-1] 

X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42, 
    stratify=y 
)

rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    oob_score=True, 
    random_state=42
)

rf_classifier.fit(X_train, y_train)

# Calculate and print OOB accuracy
oob_accuracy = rf_classifier.oob_score_
print("--- Model Performance Metrics (Random Forest) ---")
print("OOB Accuracy (Out-of-Bag Score): {:.4f}".format(oob_accuracy))

y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Test Accuracy (Random Forest Ensemble): {:.4f}".format(accuracy))

print("\n--- Detailed Test Results ---")
print(f"Number of test data points: {len(X_test)}")
print("Ground Truth (Actual Labels):\n", y_test.reset_index(drop=True))
print("Predicted Labels (Model Output):", y_pred)

print('\n--- Classification Report ---')
print("Note: '0' corresponds to 'no', '1' corresponds to 'yes' for the 'play' target.")
print(classification_report(y_test, y_pred, zero_division=0))

# Feature Importance
feature_importance = rf_classifier.feature_importances_

importance_df = pd.DataFrame(
    {'Feature': X.columns, 'Importance': feature_importance}
)

importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n--- Feature Importance ---")
print(importance_df)

plt.figure(figsize=(10, 6))
importance_df.plot(
    kind="bar", 
    x="Feature", 
    y="Importance", 
    color="lightblue",
    legend=False,
    ax=plt.gca() 
)
plt.title("Random Forest Feature Importance for Ecoli Data")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show() 

