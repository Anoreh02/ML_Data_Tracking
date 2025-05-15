import pandas as pd

# Load the datasets
df_network = pd.read_csv('session_network_features.csv')
df_behavior = pd.read_csv('session_behavior_features.csv')

print("--- Initial Shapes ---")
print(f"Network features shape: {df_network.shape}")
print(f"Behavior features shape: {df_behavior.shape}")

# Before merging, it's good to check for potential issues:
# 1. Are there duplicate 'session_start_url's in df_network?
#    If yes, merging might create more rows than in df_behavior if one behavioral
#    session's URL matches multiple network entries (this would be unusual if
#    df_network is already summarized per URL).
print(f"\nNumber of unique session_start_url in df_network: {df_network['session_start_url'].nunique()}")
if df_network['session_start_url'].duplicated().any():
    print("Warning: df_network contains duplicate 'session_start_url's. Review how network data is summarized.")
    # Example: df_network[df_network['session_start_url'].duplicated(keep=False)].sort_values('session_start_url')

# 2. Are there duplicate 'session_start_url's in df_behavior associated with *different* session_id_group?
#    This is fine, as session_id_group is the unique session identifier.
#    If 'session_start_url' itself was the unique key in df_behavior, duplicates would be an issue.
print(f"Number of unique session_start_url in df_behavior: {df_behavior['session_start_url'].nunique()}")
print(f"Number of unique session_id_group in df_behavior: {df_behavior['session_id_group'].nunique()}")


# Perform a left merge:
# Keep all rows from df_behavior (left)
# Add columns from df_network (right) where 'session_start_url' matches.
# If a 'session_start_url' in df_behavior doesn't exist in df_network,
# the new columns from df_network will have NaN (Not a Number) values for that row.
df_merged = pd.merge(
    df_behavior,
    df_network,
    on='session_start_url',  # The column to merge on
    how='left'               # Type of merge
)

print("\n--- Shape After Merge ---")
print(f"Merged dataframe shape: {df_merged.shape}")

# Check the result
print("\n--- First 5 rows of merged data ---")
print(df_merged.head())

# Check for NaNs in columns that came from df_network.
# This will tell you if any behavioral sessions didn't have a matching network entry.
print("\n--- NaN counts in merged data (especially network columns) ---")
# Pick a column that should definitely exist if the network data was merged successfully
# For example: 'net_total_requests_logged'
nan_in_network_col = df_merged['net_total_requests_logged'].isnull().sum()
if nan_in_network_col > 0:
    print(f"Warning: {nan_in_network_col} behavioral sessions did not have matching network data based on 'session_start_url'.")
    print("These rows will have NaN for network features.")
    # You can inspect these rows:
    # print(df_merged[df_merged['net_total_requests_logged'].isnull()])
else:
    print("All behavioral sessions successfully found matching network data.")

# You can also check the general NaN summary
print("\nOverall NaN counts per column in merged data:")
print(df_merged.isnull().sum())

# Verify if session_id_group is still the unique identifier for rows
if df_merged['session_id_group'].is_unique:
    print("\n'session_id_group' is still unique in the merged DataFrame.")
else:
    print("\nWarning: 'session_id_group' is NOT unique in the merged DataFrame. This might indicate an issue if df_network had multiple entries for the same session_start_url, leading to a one-to-many merge.")
    # If this happens, you might need to aggregate df_network by 'session_start_url' before merging,
    # or re-evaluate the uniqueness of your keys.

output_filename = "merged_behavior_network_data.csv"
df_merged.to_csv(output_filename, index=False)
print(f"\n--- Merged data saved to {output_filename} ---")