from flask import Flask, request, jsonify, render_template
import pickle
from preprocessing import preprocess_email
import hashlib
import random

app = Flask(__name__)

def hash_function(word, seed):
    # Generate a hash using a seed for different hash functions
    random.seed(seed)
    hash_value = hashlib.sha256((word + str(seed)).encode('utf-8')).hexdigest()
    # Convert to binary and truncate to the first 32 bits
    binary_rep = bin(int(hash_value[:8], 16))[2:].zfill(32)  # Ensure it's 32 bits
    return binary_rep

def least_significant_zero_bit_position(hash_value):
    try:
        # Reverse the binary string to find the first '0'
        return hash_value[::-1].index('0')
    except ValueError:
        # If no zero is found, return 32 (since it's a 32-bit string)
        return len(hash_value)

def flajolet_martin(text, num_hashes=20):
    max_zero_positions = [0] * num_hashes  # Keep track of max zero bit position for each hash function

    for seed in range(num_hashes):  # Use different hash functions based on seeds
        for word in text.split():  # Split the text into words
            hash_value = hash_function(word, seed)  # Get a hash value for each word using the seed
            lszb = least_significant_zero_bit_position(hash_value)  # Find least significant zero bit position
            max_zero_positions[seed] = max(max_zero_positions[seed], lszb)  # Track the max zero position

    # Harmonic mean to average the estimates
    harmonic_mean = sum([2 ** pos for pos in max_zero_positions]) / num_hashes
    return harmonic_mean if harmonic_mean < 1e18 else float('inf')  # Cap large values

# Load the Bloom filter from file
with open('models/bloom_filter.pkl', 'rb') as bf_file:
    bloom_filter = pickle.load(bf_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    email_content = request.form['email']

    # Preprocess the email content before checking
    preprocessed_email = preprocess_email(email_content)

    # Check if the email is likely spam using the Bloom filter
    is_spam = preprocessed_email in bloom_filter
    section = "Spam" if is_spam else "Normal"

    return jsonify({'result': section, 'email': email_content})

if __name__ == "__main__":
    app.run(debug=True)

