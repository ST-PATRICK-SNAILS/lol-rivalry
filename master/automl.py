import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor

# Load the data
data = pd.read_csv('masterSpreadsheet.csv')

# Assume the dataset has columns like 'TeamA_Attr1', 'TeamB_Attr1', ..., 'Outcome'
# Outcome column should be binary (0 or 1) or categorical ('Win', 'Loss')

# Split data into training and testing
train_data = data.sample(frac=0.7, random_state=42)
test_data = data.drop(train_data.index)

# Define the predictor. The label column is the one we want to predict.
label_column = 'Winner'
save_path = 'modelv1'  # specifies folder to store trained models

predictor = TabularPredictor(label=label_column, path=save_path).fit(train_data)

# Evaluate the model
performance = predictor.evaluate(test_data)

print("Model performance on test data:", performance)

# To make predictions
predictions = predictor.predict(test_data.drop(columns=[label_column]))

print("Predictions:", predictions.head())
