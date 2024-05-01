import plotly.graph_objects as go
import pandas as pd
import os
from collections import defaultdict
import csv



# Function to calculate the average duration for each key per user
def calculate_average_durations(directory='./data'):
    consolidated_data = []
    
    # List all user directories
    user_dirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    for user_dir in user_dirs:
        email = os.path.basename(user_dir)  # Assuming directory name is user's email
        keystroke_file = os.path.join(user_dir, 'filtered_keystroke_durations.csv')
        
        # Check if the specific CSV file exists
        if not os.path.exists(keystroke_file):
            continue
        
        # Initialize a dictionary to store total duration and count for each key
        key_durations = defaultdict(lambda: {'total_duration': 0, 'count': 0})
        
        # Read the keystroke durations and aggregate them
        with open(keystroke_file, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = row['Key']
                duration = int(row['Duration (ms)'])
                key_durations[key]['total_duration'] += duration
                key_durations[key]['count'] += 1
        
        # Calculate average duration for each key and prepare consolidated data
        for key, data in key_durations.items():
            average_duration = data['total_duration'] / data['count']
            consolidated_data.append({'email': email, 'key': key, 'average_duration': average_duration})
    
    return consolidated_data

# Generate the consolidated list of dictionaries
consolidated_list = calculate_average_durations()




#HeatMap creation

df = pd.DataFrame(consolidated_list)

# Use pivot_table method to ensure all emails are included
pivot_df = pd.pivot_table(df, values='average_duration', index='email', columns='key', fill_value=0)

# Proceed to generate the heatmap with Plotly
fig = go.Figure(data=go.Heatmap(
    z=pivot_df.values,
    x=pivot_df.columns,
    y=pivot_df.index,
    colorscale='Viridis', # Color scale can be adjusted
))

# Update layout for clarity and readability
fig.update_layout(
    title='Keystroke Duration Heat Map',
    xaxis_nticks=36,
    autosize=True,
    margin=dict(t=50, l=50, r=50, b=50),
    paper_bgcolor="LightSteelBlue",
)

fig.show()