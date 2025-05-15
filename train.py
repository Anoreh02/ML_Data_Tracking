import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# Load the merged data
try:
    df = pd.read_csv("merged_behavior_network_data.csv")
except FileNotFoundError:
    print("Error: 'merged_behavior_network_data.csv' not found. Make sure the file is in the correct directory.")
    exit()

print("Data loaded successfully. Shape:", df.shape)
print("First 5 rows:\n", df.head())

# --- Feature Selection ---
# Select all numerical columns that could be relevant for detecting unusual patterns.
# Exclude identifiers and potentially non-numeric columns if any were accidentally included.
identifier_cols = ['session_id_group', 'session_start_url']
features_df = df.drop(columns=identifier_cols, errors='ignore') # errors='ignore' is just in case a col is already dropped

# Ensure all selected features are numeric
numeric_features_df = features_df.select_dtypes(include=np.number)

if numeric_features_df.shape[1] == 0:
    print("Error: No numeric features found to train the model. Please check your CSV and feature selection.")
    exit()

print(f"\nSelected {numeric_features_df.shape[1]} numeric features for training.")
print("Feature columns:", numeric_features_df.columns.tolist())

# Check for NaN values in the selected features (should be 0 based on your combine.py output)
if numeric_features_df.isnull().sum().any():
    print("\nWarning: NaN values found in features. Consider imputing them.")
    # Example: numeric_features_df = numeric_features_df.fillna(numeric_features_df.mean())
    # For simplicity here, we'll proceed, but imputation is important in practice.
    # A better approach might be to drop rows with NaNs if few, or impute.
    # For now, let's just show how many NaNs per column.
    print(numeric_features_df.isnull().sum())
    # If you must proceed with NaNs for some reason and IForest supports it (depends on version/implementation details)
    # otherwise, imputation or dropping is necessary.
    # Let's assume for now combine.py ensured no NaNs in the final features.

# --- Model Training ---
# The 'contamination' parameter is the expected proportion of outliers in the data set.
# 'auto' is a common choice, or you can set a specific value like 0.01 (1%), 0.05 (5%), etc.
# This value depends on how many "unusual tracking patterns" you expect to find.
# For this research, you might need to experiment with this parameter or derive it.
# Let's start with 'auto' or a small percentage.
# If you want more sensitivity to anomalies, you might increase contamination slightly.
contamination_rate = 'auto' # or e.g., 0.05 for 5% expected outliers

# It's good practice to set a random_state for reproducibility
iso_forest = IsolationForest(n_estimators=100,         # Number of trees in the forest
                             contamination=contamination_rate,
                             random_state=42,
                             n_jobs=-1)                 # Use all available processors

print(f"\nTraining Isolation Forest with contamination='{contamination_rate}'...")
iso_forest.fit(numeric_features_df)
print("Training complete.")

# --- Getting the "Suspiciousness Score" ---
# The paper mentions "outputting a suspiciousness score per session."
# The decision_function() method provides this.
# Scores are typically such that lower scores indicate more anomalous (suspicious).
# Negative scores are outliers, positive scores are inliers.
# Scores close to -1 are strong outliers, scores close to 1 are strong inliers.
session_scores = iso_forest.decision_function(numeric_features_df)

# Add the scores back to the original DataFrame for analysis
df['iforest_suspiciousness_score'] = session_scores

# --- Getting Anomaly Predictions (Optional, based on contamination) ---
# The predict() method returns -1 for outliers (anomalies) and 1 for inliers.
# This is based on the 'contamination' threshold.
df['iforest_anomaly_prediction'] = iso_forest.predict(numeric_features_df)

# --- Analyzing the Results ---
print("\n--- Results ---")
print(df[['session_id_group', 'session_start_url', 'iforest_suspiciousness_score', 'iforest_anomaly_prediction']].head())

# See how many anomalies were detected based on the contamination rate
num_anomalies = (df['iforest_anomaly_prediction'] == -1).sum()
print(f"\nNumber of sessions flagged as anomalous (prediction = -1): {num_anomalies} out of {len(df)}")
print(f"This corresponds to {num_anomalies/len(df)*100:.2f}% of the data.")

# Display the most suspicious sessions (lowest scores)
print("\nTop 10 most suspicious sessions (lowest scores):")
print(df.sort_values(by='iforest_suspiciousness_score').head(10)[['session_id_group', 'session_start_url', 'iforest_suspiciousness_score']])

# You can save this DataFrame with scores for further analysis or as input to your supervised models
df.to_csv("merged_data_with_iforest_scores.csv", index=False)
print("\nDataFrame with Isolation Forest scores saved to 'merged_data_with_iforest_scores.csv'")