# Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = "2025_01_22_amaron_sales_sample_data.xlsx"   # Replace with your file path
data = pd.read_excel(file_path)

# Inspect the data
print(data.head())

# Step 1: Preprocessing
# Convert 'sale_date' to datetime and extract features
data['sale_date'] = pd.to_datetime(data['sale_date'])
data['year'] = data['sale_date'].dt.year
data['month'] = data['sale_date'].dt.month
data['day'] = data['sale_date'].dt.day

# Drop 'sale_id' and 'sale_date' as they are not useful for prediction
data = data.drop(columns=['sale_id', 'sale_date'])

# Separate features and target
X = data.drop(columns=['revenue'])
y = data['revenue']

# Identify categorical and numerical columns
categorical_columns = ['country', 'product_category', 'battery_type']
numerical_columns = ['units_sold', 'unit_price', 'year', 'month', 'day']

# Step 2: Create a preprocessing pipeline
categorical_transformer = OneHotEncoder(handle_unknown='ignore')
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
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the model
model.fit(X_train, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Save the model for future use
import joblib
joblib.dump(model, "sales_forecast_model.pkl")
