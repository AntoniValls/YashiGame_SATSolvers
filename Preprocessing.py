# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Dipromats 2024 challenge

# ## 1 Importing the data

# +
import pandas as pd

en_df = pd.read_json('dipromats24_t1_train_en.json')
sp_df = pd.read_json('dipromats24_t1_train_es.json')
# -

sp_df.head()

# ## 2 Analysis of the data

# ### 2.1 English

# +
num_rows, num_columns = en_df.shape

column_names = en_df.columns.tolist()

print("Number of tweets:", num_rows)
print("Number of features:", num_columns)
print("Features:", column_names)
# -

print(en_df.isna().any().any())
print(en_df.isnull().any().any())

# #### Example of an English tweet

en_df.loc[66]["text"]

# #### Visualitzation

# +
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(16, 6))

plt.subplot(1, 2, 1)
sns.countplot(x='label_task1', data=en_df)
plt.title('Task 1')
plt.xlabel('Propagandistic?')
plt.ylabel('Counts')

plt.subplot(1, 2, 2)
sns.countplot(x='country', data=en_df)
plt.title('Country')
plt.xlabel('Country')
plt.ylabel('Counts')

plt.tight_layout()
plt.show()
# -

en_df['UTC'] = pd.to_datetime(en_df['UTC'])

# +
# Set 'time' column as index if it's not already
sp_df.set_index('UTC', inplace=True)

# Resample the data to aggregate tweets by a specific time frequency, e.g., daily
# You can change 'D' to other time frequencies like 'H' for hourly, 'W' for weekly, etc.
tweet_counts = sp_df.resample('D').size()

# Plot the time evolution of tweet uploads
plt.figure(figsize=(10, 6))
tweet_counts.plot()
plt.title('Time Evolution of Tweet Uploads')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.grid(True)
plt.show()
# -

# ### 2.2 Spanish

# +
num_rows, num_columns = sp_df.shape

column_names = sp_df.columns.tolist()

print("Number of tweets:", num_rows)
print("Number of features:", num_columns)
print("Features:", column_names)
# -

# #### Example of Spanish tweet

sp_df.loc[55]["text"]

# #### Visualitzation

# +
plt.figure(figsize=(16, 6))

plt.subplot(1, 2, 1)
sns.countplot(x='label_task1', data=sp_df)
plt.title('Task 1')
plt.xlabel('Propagandistic?')
plt.ylabel('Counts')

plt.subplot(1, 2, 2)
sns.countplot(x='country', data=sp_df)
plt.title('Country')
plt.xlabel('Country')
plt.ylabel('Counts')

plt.tight_layout()
plt.show()
# -

sp_df['UTC'] = pd.to_datetime(sp_df['UTC'])

# +
# Set 'time' column as index if it's not already
sp_df.set_index('UTC', inplace=True)

# Resample the data to aggregate tweets by a specific time frequency, e.g., daily
# You can change 'D' to other time frequencies like 'H' for hourly, 'W' for weekly, etc.
tweet_counts = sp_df.resample('D').size()

# Plot the time evolution of tweet uploads
plt.figure(figsize=(10, 6))
tweet_counts.plot()
plt.title('Time Evolution of Tweet Uploads')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.grid(True)
plt.show()
