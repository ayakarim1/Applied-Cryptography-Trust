#This code includes an array that contains 10 algothims from which
#the user chooses the preferred one. It explores all the csv files 
#in a specific directory, encrypts data, performs addition, 
#and then decrypts the value and performs division since the existing 
#algorithms do not support division on encrypted data:

from lightphe import LightPHE
import csv
import os

# Specify directory containing CSV files
directory = "/home/aya/Desktop/output"

# Encryption parameters
algorithms = [
  "RSA",
  "ElGamal",
  "Exponential-ElGamal",
  "Paillier",
  "Damgard-Jurik",
  "Okamoto-Uchiyama",
  "Benaloh",
  "Naccache-Stern",
  "Goldwasser-Micali",
  "EllipticCurve-ElGamal"
]

# Initialize LightPHE instance
try:
  phe = LightPHE(algorithm_name=algorithms[2])
except ValueError as e: 
  print(f"Error: Unsupported algorithm: {algorithms[2]}. Please check LightPHE documentation for supported algorithms.")
  exit(1)

# Iterate through all CSV files
for filename in os.listdir(directory):
  if filename.endswith(".csv"):
    filepath = os.path.join(directory, filename)
    try:
      # Open and read CSV file
      with open(filepath, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row (assuming the first row is header)

        # Accumulators for sum and count
        total_sum = phe.encrypt(0)  # Initialize encrypted accumulator for sum
        total_count = 0

        # Process each data row
        for row in reader:
          if len(row) >= 2:
            try:
              # Extract and convert value from second column
              value = int(float(row[1]))

              # Homomorphic addition (accumulate encrypted values)
              encrypted_value = phe.encrypt(value)
              total_sum = total_sum + encrypted_value
              total_count += 1
            except ValueError as e:
              print(f"Error parsing value in file {filename}: {e}")
          else:
            print(f"Warning: Line with less than 2 columns in file: {filename}")

        # Calculate average after decryption
        if total_count > 0:
          decrypted_sum = phe.decrypt(total_sum)
          decrypted_average = decrypted_sum / total_count
          print(f"Decrypted average for file {filename}: {decrypted_average:.2f}")
        else:
          print(f"No valid data found in file {filename}")

    except FileNotFoundError as e:
      print(f"Error opening file: {filepath}")
