import pickle
import pandas as pd
from pybloom_live import BloomFilter
from preprocessing import preprocess_email

# Define the size of the Bloom filter and the false positive rate
bloom_filter = BloomFilter(capacity=10000, error_rate=0.001)

import pandas as pd

# Load the dataset
data = pd.read_csv('SMSSpamCollection', sep='\t', names=['label', 'message'])

# Preprocess the dataset and add spam emails to Bloom filter
for index, row in data.iterrows():
    if row['label'] == 'spam':
        cleaned_email = preprocess_email(row['message'])
        bloom_filter.add(cleaned_email)

print(f"Loaded {len(data)} messages into the Bloom filter.")


    # Save the trained Bloom filter to a pickle file
with open('models/bloom_filter.pkl', 'wb') as f:
    pickle.dump(bloom_filter, f)
print("Bloom filter created and saved to bloom_filter.pkl")