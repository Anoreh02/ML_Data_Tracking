import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# --- Configuration ---
MODEL_FILE_TO_TEST = 'trains_output/rf_model_20250515_230705.joblib' # Path to your saved model
TEST_DATA_FILE = 'path_to_your_TEST_DATA.csv' # <-- IMPORTANT: REPLACE WITH ACTUAL PATH TO YOUR TEST CSV

# This list should be the exact feature columns the model was trained on.
# It's best if this was saved during training or can be reliably reconstructed.
# For now, we'll try to get it from the model, or use a placeholder.
EXPECTED_FEATURE_COLUMNS = None # We will try to get this from the loaded model

# 1. Load the Trained Model
try:
    loaded_rf_model = joblib.load(MODEL_FILE_TO_TEST)
    print(f"Model '{MODEL_FILE_TO_TEST}' loaded successfully.")
    if hasattr(loaded_rf_model, 'feature_names_in_'):
        EXPECTED_FEATURE_COLUMNS = loaded_rf_model.feature_names_in_
        print(f"Model was trained on these {len(EXPECTED_FEATURE_COLUMNS)} features.")
    else:
        print("Warning: `feature_names_in_` not found in the model. ")
        print("You MUST ensure your test data columns match what was used for X during training.")
        # MANUALLY DEFINE `EXPECTED_FEATURE_COLUMNS` list here if needed, based on your training script's X.columns
        # Example:
        # EXPECTED_FEATURE_COLUMNS = ['num_total_events', 'num_page_visits', ..., 'iforest_suspiciousness_score']
        # For this script to run without error if feature_names_in_ is missing, provide a default or exit
        if EXPECTED_FEATURE_COLUMNS is None:
            print("Error: Cannot determine expected feature columns. Please define EXPECTED_FEATURE_COLUMNS manually.")
            exit()

except FileNotFoundError:
    print(f"Error: Model file '{MODEL_FILE_TO_TEST}' not found.")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# 2. Load and Prepare Your Test Data
try:
    df_test_full = pd.read_csv(TEST_DATA_FILE)
    print(f"\nTest data loaded from '{TEST_DATA_FILE}'. Shape: {df_test_full.shape}")
except FileNotFoundError:
    print(f"Error: Test data file '{TEST_DATA_FILE}' not found.")
    exit()
except Exception as e:
    print(f"Error loading test data: {e}")
    exit()

# Ensure 'manual_label' column exists in the test data for evaluation
target_col = 'manual_label'
if target_col not in df_test_full.columns:
    print(f"Error: Target column '{target_col}' not found in the test data file.")
    print("The test data needs ground truth labels for evaluation.")
    exit()

# Drop rows where manual_label might be missing in the test set (if any)
if df_test_full[target_col].isnull().any():
    print(f"Warning: Found {df_test_full[target_col].isnull().sum()} nulls in target column of test data. Dropping them.")
    df_test = df_test_full.dropna(subset=[target_col]).copy()
else:
    df_test = df_test_full.copy()

if df_test.empty:
    print("Error: No test data remains after handling missing labels.")
    exit()

df_test[target_col] = df_test[target_col].astype(int)

# Prepare X_test (features) and y_test (true labels)
# Ensure X_test has the exact same columns as the training data X, in the same order.
try:
    X_test = df_test[EXPECTED_FEATURE_COLUMNS]
except KeyError as e:
    print(f"Error: One or more expected feature columns not found in the test data: {e}")
    print("Make sure your test data CSV includes all necessary feature columns with correct names.")
    print(f"Expected columns: {EXPECTED_FEATURE_COLUMNS}")
    print(f"Columns found in test data: {df_test.columns.tolist()}")
    exit()

y_test = df_test[target_col]

if len(X_test) == 0:
    print("Error: No samples in X_test after feature selection.")
    exit()

print(f"Prepared {len(X_test)} samples for testing.")

# 3. Make Predictions on the Test Data
print("\nMaking predictions on the test set...")
try:
    y_pred_test = loaded_rf_model.predict(X_test)
    y_pred_proba_test = loaded_rf_model.predict_proba(X_test)[:, 1] # Probabilities for the positive class (class 1)
except Exception as e:
    print(f"Error during prediction: {e}")
    print("This might be due to a mismatch in features between training and testing data, or NaNs.")
    if X_test.isnull().values.any():
        print("NaNs detected in X_test features:")
        print(X_test.isnull().sum()[X_test.isnull().sum() > 0])
    exit()

# 4. Evaluate Model Performance
print("\n--- Test Set Performance ---")
accuracy = accuracy_score(y_test, y_pred_test)
precision = precision_score(y_test, y_pred_test, zero_division=0) # Handles cases with no predicted positives
recall = recall_score(y_test, y_pred_test, zero_division=0)       # Handles cases with no actual positives
f1 = f1_score(y_test, y_pred_test, zero_division=0)               # Handles both

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f} (Portion of predicted positives that were_correctly_positive for class 1)")
print(f"Recall:    {recall:.4f} (Portion of actual positives that were correctly identified for class 1)")
print(f"F1-score:  {f1:.4f}")

print("\nConfusion Matrix:")
# Rows: True Labels, Columns: Predicted Labels
# TN  FP
# FN  TP
cm = confusion_matrix(y_test, y_pred_test)
print(cm)
# For clarity:
if cm.shape == (2,2): # Ensure it's a 2x2 matrix
    print(f"True Negatives (TN - Correctly 0): {cm[0, 0]}")
    print(f"False Positives (FP - Incorrectly 1, Type I error): {cm[0, 1]}")
    print(f"False Negatives (FN - Incorrectly 0, Type II error): {cm[1, 0]}")
    print(f"True Positives (TP - Correctly 1): {cm[1, 1]}")
else:
    print("Confusion matrix is not 2x2. Check class balance or predictions.")


print("\nClassification Report:")
try:
    # target_names based on your labels 0 and 1
    print(classification_report(y_test, y_pred_test, target_names=['Class 0 (Legit)', 'Class 1 (Tracking)'], zero_division=0))
except ValueError as e:
    print(f"Could not generate classification report: {e}")
    print("This can happen if one class is entirely absent in y_true or y_pred in a way that makes metrics undefined.")


# (Optional) Save test predictions alongside true labels for further analysis
df_test_predictions = X_test.copy()
df_test_predictions['true_label'] = y_test
df_test_predictions['predicted_label'] = y_pred_test
df_test_predictions['predicted_proba_class1'] = y_pred_proba_test
# Add session_id_group and url back if you want for easier identification
if 'session_id_group' in df_test.columns:
    df_test_predictions.insert(0, 'session_id_group', df_test['session_id_group'])
if 'session_start_url' in df_test.columns:
    df_test_predictions.insert(1, 'session_start_url', df_test['session_start_url'])

predictions_output_file = f"test_predictions_for_model_{MODEL_FILE_TO_TEST.split('/')[-1].replace('.joblib','')}.csv"
try:
    df_test_predictions.to_csv(predictions_output_file, index=False)
    print(f"\nTest predictions saved to: {predictions_output_file}")
except Exception as e:
    print(f"Error saving test predictions: {e}")