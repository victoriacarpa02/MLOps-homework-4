#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sklearn

print("scikit-learn:", sklearn.__version__)


# In[2]:


import sys

print("Python:", sys.version)
print("Python executable:", sys.executable)


# In[3]:


import pickle
import pandas as pd


# In[4]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[5]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[6]:


year = 2023
month = 3

input_file = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    f"yellow_tripdata_{year:04d}-{month:02d}.parquet"
)

df = read_data(input_file)

print("Period:", f"{year:04d}-{month:02d}")
print("Prepared rows:", len(df))


# In[7]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[8]:


print("Period:", f"{year:04d}-{month:02d}")
print("Predictions:", len(y_pred))
print("Q1 standard deviation:", y_pred.std())


# In[9]:


df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

df_result = pd.DataFrame({
    "ride_id": df["ride_id"],
    "predicted_duration": y_pred,
})

df_result.head()


# In[10]:


from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"predictions_{year:04d}-{month:02d}.parquet"

df_result.to_parquet(
    output_file,
    engine="pyarrow",
    compression=None,
    index=False,
)

size_bytes = output_file.stat().st_size

print("Output file:", output_file)
print("Rows:", len(df_result))
print("Columns:", df_result.columns.tolist())
print("Size in bytes:", size_bytes)
print(f"Size in MiB: {size_bytes / (1024 ** 2):.2f}")


# In[ ]:




