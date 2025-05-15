import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split # Not used yet for training
from sklearn.model_selection import cross_val_score, KFold # For cross-validation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score # For detailed metrics
import numpy as np
import joblib
import os
import csv
from datetime import datetime

# --- Configuration for Output ---
OUTPUT_BASE_FOLDER = "trains_output"
os.makedirs(OUTPUT_BASE_FOLDER, exist_ok=True) # Create the base folder if it doesn't exist

# Generate a unique timestamp for this specific training run
RUN_TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# Define file paths for this run
MODEL_FILENAME = os.path.join(OUTPUT_BASE_FOLDER, f"rf_model_{RUN_TIMESTAMP}.joblib")
RESULTS_CSV_FILE = os.path.join(OUTPUT_BASE_FOLDER, "training_runs_summary.csv")
FEATURE_IMPORTANCE_CSV_FILE = os.path.join(OUTPUT_BASE_FOLDER, f"feature_importances_{RUN_TIMESTAMP}.csv")


# 1. Load your LABELED data
try:
    df_labeled = pd.read_csv("labeled_merged_data_with_iforest_scores.csv") # Make sure this is your fully labeled file
except FileNotFoundError:
    print("Error: 'labeled_merged_data_with_iforest_scores.csv' not found.")
    exit()

print(f"Labeled data loaded. Shape: {df_labeled.shape}")

# 2. Prepare data for training (ensure all rows intended for training have labels)
if df_labeled['manual_label'].isnull().any():
    print(f"Warning: Found {df_labeled['manual_label'].isnull().sum()} rows with no manual label. These will be excluded.")
    df_train = df_labeled.dropna(subset=['manual_label']).copy()
else:
    df_train = df_labeled.copy()

if len(df_train) < 10: # Arbitrary threshold for minimum samples
    print(f"Error: Only {len(df_train)} manually labeled samples available. Need more data for meaningful training.")
    exit()

df_train['manual_label'] = df_train['manual_label'].astype(int)
print(f"Using {len(df_train)} manually labeled samples for training and cross-validation.")

# Define features (X) and target (y)
identifier_cols = ['session_id_group', 'session_start_url']
target_col = 'manual_label'
# Exclude iforest_anomaly_prediction as its derived from the score which is already a feature
cols_to_drop_for_X = identifier_cols + [target_col, 'iforest_anomaly_prediction']
potential_features_df = df_train.drop(columns=cols_to_drop_for_X, errors='ignore')
X = potential_features_df.select_dtypes(include=np.number)

# Ensure iforest_suspiciousness_score is present if it wasn't dropped and exists
if 'iforest_suspiciousness_score' not in X.columns and 'iforest_suspiciousness_score' in df_train.columns:
    X['iforest_suspiciousness_score'] = df_train['iforest_suspiciousness_score']

y = df_train[target_col]

# Basic checks
if X.empty or len(X.columns) == 0:
    print("Error: No features selected for X.")
    exit()
if len(y) == 0 :
    print("Error: Target variable y is empty.")
    exit()
if len(X) != len(y):
    print(f"Error: Mismatch in length of X ({len(X)}) and y ({len(y)}).")
    exit()
if y.nunique() < 2:
    print(f"Error: Target variable y has only {y.nunique()} unique value(s). Needs at least 2 for classification.")
    exit()

print(f"\nSelected {X.shape[1]} features for supervised training.")
# print("Feature columns for Random Forest:", X.columns.tolist()) # Can be long
print(f"Target variable 'manual_label' has {y.nunique()} unique classes: {y.unique()}")
print(f"Class distribution: \n{y.value_counts(normalize=True)}")


# 3. Train a Random Forest Classifier (this will be the final model for saving)
# Consider class_weight='balanced' especially if your classes are imbalanced
rf_model_final = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
print("\nTraining final Random Forest model on all labeled data...")
try:
    rf_model_final.fit(X, y)
    print("Final Random Forest training complete.")
except ValueError as e:
    print(f"Error during final Random Forest training: {e}")
    exit()

# --- SAVE THE TRAINED RANDOM FOREST MODEL ---
try:
    joblib.dump(rf_model_final, MODEL_FILENAME)
    print(f"\nTrained Random Forest model saved to: {MODEL_FILENAME}")
except Exception as e:
    print(f"Error saving model: {e}")

# 4. Evaluation
# A. Accuracy on the entire training set (use with caution, prone to overfitting)
y_pred_full_train = rf_model_final.predict(X)
train_accuracy_full = accuracy_score(y, y_pred_full_train)
print(f"\nAccuracy on the full {len(X)} training samples: {train_accuracy_full:.4f}")
print("(Note: This is on training data and likely optimistic.)")

# B. Cross-Validation for a more robust performance estimate
n_splits_cv = 5 # Or 10, or StratifiedKFold if classes are very imbalanced
if len(df_train) >= n_splits_cv * 2 : # Ensure enough samples for CV
    print(f"\nPerforming {n_splits_cv}-Fold Cross-Validation...")
    # Use a new model instance for CV to avoid data leakage from rf_model_final if it was already fit
    rf_model_cv = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    kf = KFold(n_splits=n_splits_cv, shuffle=True, random_state=123) # StratifiedKFold might be better

    cv_accuracy = cross_val_score(rf_model_cv, X, y, cv=kf, scoring='accuracy')
    cv_precision = cross_val_score(rf_model_cv, X, y, cv=kf, scoring='precision') # Precision for class 1
    cv_recall = cross_val_score(rf_model_cv, X, y, cv=kf, scoring='recall')    # Recall for class 1
    cv_f1 = cross_val_score(rf_model_cv, X, y, cv=kf, scoring='f1')          # F1 for class 1

    mean_cv_accuracy = cv_accuracy.mean()
    mean_cv_precision = cv_precision.mean()
    mean_cv_recall = cv_recall.mean()
    mean_cv_f1 = cv_f1.mean()

    print(f"Mean CV Accuracy: {mean_cv_accuracy:.4f}")
    print(f"Mean CV Precision (for class 1): {mean_cv_precision:.4f}")
    print(f"Mean CV Recall (for class 1): {mean_cv_recall:.4f}")
    print(f"Mean CV F1-score (for class 1): {mean_cv_f1:.4f}")
else:
    print(f"\nDataset too small ({len(df_train)} samples) for meaningful {n_splits_cv}-fold cross-validation.")
    mean_cv_accuracy, mean_cv_precision, mean_cv_recall, mean_cv_f1 = np.nan, np.nan, np.nan, np.nan


# C. Feature Importances from the final model
importances = rf_model_final.feature_importances_
feature_names = X.columns
feature_importance_data = []
print("\nTop 15 Feature Importances (from final model):")
for i in np.argsort(importances)[::-1][:15]: # Display top 15
    print(f"{feature_names[i]}: {importances[i]:.4f}")
    feature_importance_data.append({'run_timestamp': RUN_TIMESTAMP, 'feature_name': feature_names[i], 'importance': importances[i]})

# Save all feature importances for this run
feature_importance_df = pd.DataFrame({'feature_name': feature_names, 'importance': importances})
feature_importance_df.sort_values(by='importance', ascending=False, inplace=True)
try:
    feature_importance_df.to_csv(FEATURE_IMPORTANCE_CSV_FILE, index=False)
    print(f"\nFull feature importances for this run saved to: {FEATURE_IMPORTANCE_CSV_FILE}")
except Exception as e:
    print(f"Error saving feature importances: {e}")


# 5. Log results to the summary CSV
results_summary_header = [
    'run_timestamp', 'model_filename', 'num_training_samples', 'num_features',
    'class_0_count', 'class_1_count',
    'train_accuracy_full_set',
    'cv_mean_accuracy', 'cv_mean_precision', 'cv_mean_recall', 'cv_mean_f1',
    'rf_n_estimators', 'rf_class_weight'
]
class_counts = y.value_counts()
results_summary_data = [
    RUN_TIMESTAMP, MODEL_FILENAME, len(X), X.shape[1],
    class_counts.get(0, 0), class_counts.get(1, 0),
    train_accuracy_full,
    mean_cv_accuracy, mean_cv_precision, mean_cv_recall, mean_cv_f1,
    rf_model_final.get_params()['n_estimators'], str(rf_model_final.get_params()['class_weight'])
]

try:
    file_exists = os.path.isfile(RESULTS_CSV_FILE)
    with open(RESULTS_CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(results_summary_header) # Write header if file is new
        writer.writerow(results_summary_data)
    print(f"\nResults summary for this run appended to: {RESULTS_CSV_FILE}")
except Exception as e:
    print(f"Error writing to results summary CSV: {e}")