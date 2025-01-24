# %%
import boto3
import os
from datetime import datetime

def upload_to_s3(file_path, bucket_name, s3_key_prefix):
    s3_client = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y_%m_%d')
    file_name = os.path.basename(file_path)
    s3_key = f"{s3_key_prefix}/{timestamp}_{file_name}"
    
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File uploaded successfully to S3: {s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")


file_path =r"C:\Users\viral\Desktop\project amaron - Copy\amaron_sales_sample_data.xlsx"
bucket_name = "amaron-client-bucket1"       
s3_key_prefix = "amaron-fles1"    

upload_to_s3(file_path, bucket_name, s3_key_prefix)


# %%
import boto3
import os

def get_latest_file_from_s3(bucket_name, s3_key_prefix, local_download_path):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_key_prefix)
    
    all_files = response.get('Contents', [])
    latest_file = max(all_files, key=lambda x: x['LastModified'])
    file_key = latest_file['Key']
    local_file_path = os.path.join(local_download_path, os.path.basename(file_key))
    
    try:
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print(f"Downloaded file: {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

bucket_name = "amaron-client-bucket1"      
s3_key_prefix = "amaron-fles1"    

local_download_path =r"C:\Users\viral\Desktop\PROJECT A"

get_latest_file_from_s3(bucket_name, s3_key_prefix, local_download_path)


# %%


# %%
import pandas as pd
import matplotlib.pyplot as plt


# %%
file_path = "2025_01_22_amaron_sales_sample_data.xlsx" 
data = pd.read_excel(file_path)

# %%
print("Data Overview:")
print(data.head())

# %%
print("\nSummary Statistics:")
print(data.describe())

# %%
print("\nMissing Values:")
print(data.isnull().sum())

# %%
# Grouping and aggregations
# Total revenue by country
data["Total Revenue"] = data["unit_price"] * data["units_sold"]
revenue_by_country = data.groupby("country")["Total Revenue"].sum()
print("\nRevenue by Country:")
print(revenue_by_country)

# %%
# Visualization: Revenue by Country
plt.figure(figsize=(10, 6))
revenue_by_country.sort_values(ascending=False).plot(kind="bar", color="skyblue")
plt.title("Revenue by Country")
plt.ylabel("Total Revenue")
plt.xlabel("Country")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# Revenue by Product Category
revenue_by_category = data.groupby("product_category")["Total Revenue"].sum()
print("\nRevenue by Product Category:")
print(revenue_by_category)

# %%
# Visualization: Revenue by Product Category
plt.figure(figsize=(8, 5))
revenue_by_category.sort_values(ascending=False).plot(kind="bar", color="green")
plt.title("Revenue by Product Category")
plt.ylabel("Total Revenue")
plt.xlabel("Product Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Units Sold by Battery Type
units_by_battery = data.groupby("battery_type")["units_sold"].sum()
print("\nUnits Sold by Battery Type:")
print(units_by_battery)



# %%
# Visualization: Units Sold by Battery Type
plt.figure(figsize=(8, 5))
units_by_battery.sort_values(ascending=False).plot(kind="bar", color="orange")
plt.title("Units Sold by Battery Type")
plt.ylabel("Total Units Sold")
plt.xlabel("Battery Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%



