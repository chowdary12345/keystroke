import csv
import os
from collections import defaultdict
import numpy as np

def read_durations(filename):
    durations = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Key']
            duration = float(row['Average Duration (ms)'])
            durations[key] = duration
    return durations

def calculate_similarity(durations1, durations2):
    # Using Euclidean distance to calculate similarity
    keys = set(durations1.keys()).intersection(durations2.keys())
    if not keys:
        return float('inf')
    return np.sqrt(sum((durations1[key] - durations2[key])**2 for key in keys))

def find_closest_match(base_directory, sample_filepath):
    sample_durations = read_durations(sample_filepath)
    min_distance = float('inf')
    closest_match = None
    emails = os.listdir(base_directory)
    emails.remove('unnamed')
    for email in emails:
        dir_path = os.path.join(base_directory, email)
        if os.path.isdir(dir_path):
            filepath = os.path.join(dir_path, 'average_keystroke_durations.csv')
            if os.path.exists(filepath):
                durations = read_durations(filepath)
                distance = calculate_similarity(sample_durations, durations)
                if distance < min_distance:
                    min_distance = distance
                    closest_match = email

    return closest_match


base_directory = './data'
sample_filepath = './data/unnamed/average_keystroke_durations.csv'
closest_match = find_closest_match(base_directory, sample_filepath)
print(f"The closest matching email directory is: {closest_match}")
