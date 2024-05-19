import pandas as pd
from autogluon.tabular import TabularPredictor

# Load the trained model
predictor = TabularPredictor.load("modelv1")

# Read the CSV file
data = pd.read_csv("masterSpreadsheet.csv")

# Ensure the actual target values are present in the data
# Replace 'target_column_name' with the actual name of the target column in your CSV
target_column = 'Winner'
if target_column not in data.columns:
    raise ValueError(f"Target column '{target_column}' not found in the data.")

# Separate features and target
features = data.drop(columns=[target_column])
actual_values = data[target_column]

# Make predictions on the entire dataset
predictions = predictor.predict(features)

# Convert predictions to binary votes
binary_votes = (predictions > 0.5).astype(int)

# Compare predictions to actual values
correct_predictions = (binary_votes == actual_values).sum()
total_predictions = len(actual_values)
accuracy = correct_predictions / total_predictions

# Print the results
print(f"Total predictions: {total_predictions}")
print(f"Correct predictions: {correct_predictions}")
print(f"Accuracy: {accuracy:.2%}")

# # Save the predictions and votes to a new CSV file (optional)
# data['Predictions'] = predictions
# data['BinaryVotes'] = binary_votes
# data.to_csv("masterSpreadsheet_with_predictions_and_votes.csv", index=False)
#
# print("Predictions and votes saved to masterSpreadsheet_with_predictions_and_votes.csv")
