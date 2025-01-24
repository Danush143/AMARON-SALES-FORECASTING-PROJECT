# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the data
file_path = "2025_01_22_amaron_sales_sample_data.xlsx"  # Replace with your file path
data = pd.read_excel(file_path)

# Inspect the data
print("Dataset Overview:")
print(data.info())
print("\nFirst 5 Rows:")
print(data.head())

# Step 1: Preprocessing
# Convert 'sale_date' to datetime and extract features
data['sale_date'] = pd.to_datetime(data['sale_date'], errors='coerce')  # Handle parsing errors
data['year'] = data['sale_date'].dt.year
data['month'] = data['sale_date'].dt.month
data['day'] = data['sale_date'].dt.day

# Drop 'sale_id' and 'sale_date' as they are not useful for prediction
data = data.drop(columns=['sale_id', 'sale_date'])

# Check for missing values and handle them
if data.isnull().sum().any():
    print("\nMissing Values Detected:")
    print(data.isnull().sum())
    data = data.dropna()  # Drop rows with missing values for simplicity

# Separate features and target
X = data.drop(columns=['revenue'])
y = data['revenue']

# Identify categorical and numerical columns
categorical_columns = [col for col in X.columns if X[col].dtype == 'object']
numerical_columns = [col for col in X.columns if X[col].dtype != 'object']

# Step 2: Create a preprocessing pipeline
categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)  # Set sparse=False for better readability
numerical_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_columns),
        ('cat', categorical_transformer, categorical_columns)
    ]
)

# Step 3: Build the full pipeline with a RandomForestRegressor
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=150, random_state=42))  # Increased estimators for better performance
])

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the model
model.fit(X_train, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

# Save the model for future use
joblib.dump(model, "sales_forecast_model.pkl")
print("\nModel saved as 'sales_forecast_model.pkl'")
