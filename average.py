#This code calculates the average of the values in the csv files 
#in a specific directory without using homomorphic encryption:
import os
import pandas as pd

directory = '/home/aya/Desktop/output'
column_averages = {}

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        if 'FinapresBP' in df.columns:
            column_averages[filename] = df['FinapresBP'].mean()

for filename, average in column_averages.items():
    print(f'Average for file {filename}: {average}') 
