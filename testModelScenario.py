import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import os

# --- Configuration ---
# Path to the specific Random Forest model you want to test
MODEL_TO_TEST_FILENAME = 'trains_output/rf_model_20250515_230705.joblib' # Make sure this path is correct

# Path to your prepared test data CSV (after feature engineering and adding IF score)
# This file MUST contain the ground truth 'manual_label' column for evaluation.
TEST_DATA_CSV = 'path_to_your/PREPARED_TEST_DATA_WITH_FEATURES_AND_LABELS.csv' # <--- REPLACE THIS

EXPECTED_FEATURE_COLUMNS = None # Will be populated from the loaded model

# --- 1. Load the Trained Random Forest Model ---
if not os.path.exists(MODEL_TO_TEST_FILENAME):
    print(f"Error: Model file '{MODEL_TO_TEST_FILENAME}' not found.")
    exit()
try:
    loaded_rf_model = joblib.load(MODEL_TO_TEST_FILENAME)
    print(f"Model '{MODEL_TO_TEST_FILENAME}' loaded successfully.")
    if hasattr(loaded_rf_model, 'feature_names_in_'):
        EXPECTED_FEATURE_COLUMNS = loaded_rf_model.feature_names_in_
        print(f"Model was trained on {len(EXPECTED_FEATURE_COLUMNS)} features.")
    else:
        print("Warning: `feature_names_in_` not found in the model. You must manually define EXPECTED_FEATURE_COLUMNS.")
        # Example: EXPECTED_FEATURE_COLUMNS = ['feat1', 'feat2', ..., 'iforest_suspiciousness_score']
        # If not defined, the script might fail later.
        if EXPECTED_FEATURE_COLUMNS is None:
             print("Error: EXPECTED_FEATURE_COLUMNS is not set. Please define it manually based on training features.")
             exit()
except Exception as e:
    print(f"Error loading model '{MODEL_TO_TEST_FILENAME}': {e}")
    exit()

# --- 2. Load and Prepare Test Data ---
if not os.path.exists(TEST_DATA_CSV):
    print(f"Error: Test data file '{TEST_DATA_CSV}' not found.")
    exit()
try:
    df_test_full = pd.read_csv(TEST_DATA_CSV)
    print(f"\nTest data loaded from '{TEST_DATA_CSV}'. Shape: {df_test_full.shape}")
except Exception as e:
    print(f"Error loading test data CSV: {e}")
    exit()

target_col = 'manual_label'
if target_col not in df_test_full.columns:
    print(f"Error: Ground truth target column '{target_col}' not found in '{TEST_DATA_CSV}'.")
    exit()

# Drop rows with missing ground truth labels, if any
df_test = df_test_full.dropna(subset=[target_col]).copy()
if len(df_test) != len(df_test_full):
    print(f"Dropped {len(df_test_full) - len(df_test)} rows from test data due to missing manual_labels.")

if df_test.empty:
    print("Error: No test data available after handling missing labels.")
    exit()

df_test[target_col] = df_test[target_col].astype(int)

# Extract features (X_test) and true labels (y_test)
try:
    X_test = df_test[EXPECTED_FEATURE_COLUMNS]
except KeyError as e:
    print(f"KeyError: One or more expected feature columns not found in the test data: {e}")
    print(f"Expected features by the model: {list(EXPECTED_FEATURE_COLUMNS)}")
    print(f"Columns available in test data: {df_test.columns.tolist()}")
    print("Ensure your test data CSV has all the features the model was trained on.")
    exit()

y_test = df_test[target_col]

print(f"Prepared {len(X_test)} samples for testing.")
if X_test.isnull().values.any():
    print("Warning: NaNs found in X_test features. Predictions may fail or be inaccurate.")
    print(X_test.isnull().sum()[X_test.isnull().sum() > 0])
    # Consider imputing NaNs in X_test based on training data's statistics if this occurs.

# --- 3. Make Predictions ---
print("\nMaking predictions on the test set...")
try:
    y_pred_test = loaded_rf_model.predict(X_test)
    y_pred_proba_test = loaded_rf_model.predict_proba(X_test)[:, 1] # Prob for positive class
except Exception as e:
    print(f"Error during prediction: {e}")
    exit()

# --- 4. Evaluate Model Performance ---
print("\n--- Test Set Performance Metrics ---")
accuracy = accuracy_score(y_test, y_pred_test)
precision = precision_score(y_test, y_pred_test, zero_division=0)
recall = recall_score(y_test, y_pred_test, zero_division=0)
f1 = f1_score(y_test, y_pred_test, zero_division=0)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")

print("\nConfusion Matrix (Rows: True, Cols: Predicted):")
cm = confusion_matrix(y_test, y_pred_test)
print(cm)
if cm.shape == (2,2):
    print(f"  TN: {cm[0,0]}  FP: {cm[0,1]}")
    print(f"  FN: {cm[1,0]}  TP: {cm[1,1]}")

print("\nClassification Report:")
# Ensure there are predicted samples for both classes if possible, or handle warnings
if len(np.unique(y_pred_test)) < 2 or len(np.unique(y_test)) < 2 :
    print("Warning: Not all classes might be present in true labels or predictions of the test set.")
    print(f"Unique true labels in test: {np.unique(y_test)}")
    print(f"Unique predicted labels in test: {np.unique(y_pred_test)}")

print(classification_report(y_test, y_pred_test, target_names=['Class 0 (Legit)', 'Class 1 (Tracking)'], zero_division=0))

# --- 5. (Optional) Save Predictions ---
# Add back identifiers for easier analysis
df_results = pd.DataFrame({
    'session_id_group': df_test.get('session_id_group', pd.Series(index=df_test.index, dtype='object')),
    'session_start_url': df_test.get('session_start_url', pd.Series(index=df_test.index, dtype='object')),
    'true_label': y_test,
    'predicted_label': y_pred_test,
    'predicted_proba_class1': y_pred_proba_test
})

# Concatenate features for full context
# Ensure indices align if X_test was modified (e.g. NaNs dropped differently than df_test)
# X_test.reset_index(drop=True, inplace=True) # If X_test index might be misaligned
# df_results.reset_index(drop=True, inplace=True)
# df_results = pd.concat([df_results, X_test.reset_index(drop=True)], axis=1)


output_predictions_csv = f"test_results_for_{os.path.basename(MODEL_TO_TEST_FILENAME).replace('.joblib','')}.csv"
try:
    df_results.to_csv(output_predictions_csv, index=False)
    print(f"\nTest results and predictions saved to: {output_predictions_csv}")
except Exception as e:
    print(f"Error saving test results: {e}")