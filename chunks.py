import pickle
import gzip
import os

# Load the original pickle file
with open('similarity.pkl', 'rb') as f:
    data = f.read()  # Read the full binary data

# Define chunk size (max 24MB to be safe)
chunk_size = 24 * 1024 * 1024  # 24MB
total_size = len(data)
num_chunks = (total_size // chunk_size) + 1  # Calculate total chunks

# Save the chunks separately
for i in range(num_chunks):
    chunk = data[i * chunk_size: (i + 1) * chunk_size]

    # Save each part as a gzip-compressed file
    with gzip.open(f'similarity_part_{i + 1}.pkl.gz', 'wb') as f:
        f.write(chunk)

print(f'Split the file into {num_chunks} parts.')