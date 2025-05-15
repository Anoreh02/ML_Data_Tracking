import pandas as pd
import numpy as np
import joblib # To load the model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# --- Configuration ---
# 1. PATH TO YOUR SAVED MODEL
MODEL_PATH = 'trains_output/rf_model_20250515_230705.joblib' # Make sure this is correct

# 2. PATH TO YOUR PREPARED TEST DATA CSV
# This CSV contains new, unseen data with the same features as the training data,
# PLUS a 'manual_label' column with the true answers for these test cases.
TEST_DATA_PATH = 'my_openwpm_test_set_with_features_and_labels.csv' # <-- YOU WILL CREATE THIS FILE

# 3. LIST OF FEATURE NAMES (VERY IMPORTANT)
# These must be the exact feature names (and in the same order ideally, though pandas handles by name)
# that the model was trained on.
# If your model object (loaded_rf_model) has '.feature_names_in_', we can use that.
# Otherwise, you MUST provide this list manually.
EXPECTED_FEATURES = None 
# Example if you need to set it manually:
# EXPECTED_FEATURES = ['num_total_events', 'num_page_visits', ..., 'iforest_suspiciousness_score']

# --- Step 1: Load the Trained Model ---
try:
    loaded_rf_model = joblib.load(MODEL_PATH)
    print(f"Successfully loaded model from: {MODEL_PATH}")

    # Try to get feature names from the model if available (sklearn >= 0.24 usually)
    if hasattr(loaded_rf_model, 'feature_names_in_'):
        EXPECTED_FEATURES = loaded_rf_model.feature_names_in_
        print(f"Model was trained on {len(EXPECTED_FEATURES)} features.")
    elif EXPECTED_FEATURES is None: # If not in model and not manually set above
        print(f"Error: Could not determine feature names from the model and EXPECTED_FEATURES is not set.")
        print(f"Please define the EXPECTED_FEATURES list manually in this script.")
        exit()
    else:
        print(f"Using manually defined EXPECTED_FEATURES list with {len(EXPECTED_FEATURES)} features.")

except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# --- Step 2: Load and Prepare the Test Data ---
try:
    df_test = pd.read_csv(TEST_DATA_PATH)
    print(f"\nSuccessfully loaded test data from: {TEST_DATA_PATH}")
    print(f"Test data shape: {df_test.shape}")
except FileNotFoundError:
    print(f"Error: Test data file not found at {TEST_DATA_PATH}")
    exit()
except Exception as e:
    print(f"Error loading test data: {e}")
    exit()

# Ensure the ground truth label column exists
if 'manual_label' not in df_test.columns:
    print(f"Error: The test data CSV must contain a 'manual_label' column for ground truth.")
    exit()

# Handle any missing labels in the test set (should ideally be none for a test set)
if df_test['manual_label'].isnull().any():
    print(f"Warning: Test data 'manual_label' column contains "
          f"{df_test['manual_label'].isnull().sum()} missing values. Dropping these rows.")
    df_test.dropna(subset=['manual_label'], inplace=True)

if df_test.empty:
    print("Error: No data remains in the test set after handling missing labels.")
    exit()

df_test['manual_label'] = df_test['manual_label'].astype(int)

# Separate features (X_test) and true labels (y_test)
try:
    X_test = df_test[EXPECTED_FEATURES]
    y_test = df_test['manual_label']
except KeyError as e:
    print(f"KeyError: One or more expected feature columns not found in the test data CSV: {e}")
    print(f"Model expects features: {list(EXPECTED_FEATURES)}")
    print(f"Test data has columns: {df_test.columns.tolist()}")
    exit()

# Check for NaNs in features, as this can cause errors during prediction
if X_test.isnull().values.any():
    print("\nWarning: NaNs found in test data features (X_test). This might cause prediction errors.")
    print("Consider imputing these NaNs based on statistics from your training data.")
    # Example: X_test = X_test.fillna(X_train.mean()) # But you need X_train's mean here
    print(X_test.isnull().sum()[X_test.isnull().sum() > 0])
    # For now, we'll proceed, but this is a potential issue.

print(f"\nPrepared {len(X_test)} samples from the test set for evaluation.")

# --- Step 3: Make Predictions on the Test Data ---
try:
    y_pred = loaded_rf_model.predict(X_test)
    # Get probabilities for the positive class (class 1)
    y_pred_proba = loaded_rf_model.predict_proba(X_test)[:, 1]
except Exception as e:
    print(f"Error during model prediction: {e}")
    print("This often happens if test features don't match training features, or due to NaNs.")
    exit()

# --- Step 4: Evaluate the Predictions ---
print("\n--- MODEL PERFORMANCE ON TEST SET ---")
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f} (How many selected items are relevant for class 1?)")
print(f"Recall:    {recall:.4f} (How many relevant items are selected for class 1?)")
print(f"F1-Score:  {f1:.4f} (Harmonic mean of Precision and Recall for class 1)")

print("\nConfusion Matrix (Rows: True Label, Columns: Predicted Label):")
cm = confusion_matrix(y_test, y_pred)
print(cm)
if cm.shape == (2,2): # If binary classification and both classes are present
    print(f"  TN (True Negatives - Correctly Legit): {cm[0, 0]}")
    print(f"  FP (False Positives - Legit predicted as Tracking): {cm[0, 1]}")
    print(f"  FN (False Negatives - Tracking predicted as Legit): {cm[1, 0]}")
    print(f"  TP (True Positives - Correctly Tracking): {cm[1, 1]}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Class 0 (Legit)', 'Class 1 (Tracking)'], zero_division=0))

# You can also save these test predictions for more detailed error analysis
df_test['predicted_label'] = y_pred
df_test['predicted_proba_class1'] = y_pred_proba
df_test.to_csv('test_set_predictions_output.csv', index=False)
print("\nTest predictions (including probabilities) saved to test_set_predictions_output.csv")