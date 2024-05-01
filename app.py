from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
import csv
import os
import numpy as np
from collections import defaultdict
import csv
import os
from collections import defaultdict
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def email_page():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('phrase_page'))
    
    message = session.pop('message', '')
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Input</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <style>
        body { display: flex; justify-content: center; margin-top: 50px; }
        .container { width: 90%; max-width: 400px; }
    </style>
</head>
<body>
<div class="container">
    <h4 class="header">Enter Email</h4>
    {% if message %}
    <div class="card-panel teal lighten-2">{{ message }}</div>
    {% endif %}
    <form method="POST" class="col s12">
        <div class="row">
            <div class="input-field col s12">
                <input type="email" id="email" name="email" class="validate" required>
                <label for="email">Email</label>
            </div>
        </div>
        <button type="submit" class="waves-effect waves-light btn">Next</button>
    </form>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</body>
</html>
    """, message=message)

@app.route('/unnamed', methods=['GET', 'POST'])
def unnamed_page():
    if request.method == 'POST':
        phrase = request.form['phrase']
        keystroke_data = request.form['keystrokeData']

        # Check if the input phrase matches the required phrase
        if phrase != "The quick brown fox jumps over the lazy dog":
            flash('Please ensure the input matches the exact phrase required.')
            return redirect(url_for('unnamed_page'))
        
        # Process and save data for hypothetical 'unnamed' user
        email = 'unnamed'
        save_data(email, phrase, keystroke_data)
        calculate_average_durations(email)
        closest_email = find_closest_match('./data', f'./data/{email}/average_keystroke_durations.csv')
        flash(f'The closest matching email directory is: {closest_email}')
        return redirect(url_for('unnamed_page'))

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unnamed Input</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <style>
        body { display: flex; justify-content: center; margin-top: 20px; }
        .container { width: 90%; max-width: 600px; }
    </style>
    <script>
        let keystrokes = [];

        function recordKeystroke(event, keyAction) {
            keystrokes.push({key: event.key, action: keyAction, time: Date.now()});
        }

        function preventPaste(event) {
            event.preventDefault();
            M.toast({html: 'Please type the phrase manually.'});
        }

        function prepareData() {
            document.getElementById('keystrokeData').value = JSON.stringify(keystrokes);
        }
    </script>
</head>
<body>
<div class="container">
    <h4 class="header">Please Type the Following Phrase:</h4>
    <h5>"The quick brown fox jumps over the lazy dog"</h5>
    {% for message in get_flashed_messages() %}
    <div class="card-panel red lighten-2">{{ message }}</div>
    {% endfor %}
    <form method="POST" onsubmit="prepareData()">
        <div class="input-field">
            <input type="text" name="phrase" id="phrase" onkeydown="recordKeystroke(event, 'down');" onkeyup="recordKeystroke(event, 'up');" onpaste="preventPaste(event)" autocomplete="off" required>
            <label for="phrase">Phrase</label>
        </div>
        <input type="hidden" id="keystrokeData" name="keystrokeData">
        <button type="submit" class="btn">Submit</button>
    </form>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</body>
</html>
    """)

@app.route('/phrase', methods=['GET', 'POST'])
def phrase_page():
    if 'email' not in session:
        return redirect(url_for('email_page'))
    
    if request.method == 'POST':
        phrases = [request.form[f'phrase{i}'] for i in range(1, 6)]
        keystroke_data = request.form['keystrokeData']
        
        if not all(phrases[0] == phrase for phrase in phrases) or not all(phrases):
            flash('All inputs must contain the same phrase and none should be blank.')
            return redirect(url_for('phrase_page'))
        
        save_data(session['email'], phrases, keystroke_data)
        calculate_average_durations(session['email'])
        session['message'] = 'Phrases submitted successfully!'
        return redirect(url_for('email_page'))
    
    return render_template_string("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phrase Input</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <style>
        body { display: flex; justify-content: center; margin-top: 20px; }
        .container { width: 90%; max-width: 600px; }
        .input-field input:focus { border-bottom: 1px solid #26a69a !important; box-shadow: 0 1px 0 0 #26a69a !important; }
    </style>
    <script>
        let keystrokes = [];

        function recordKeystroke(event, keyAction) {
            keystrokes.push({key: event.key, action: keyAction, time: Date.now()});
        }

        function preventPaste(event) {
            event.preventDefault();
            M.toast({html: 'Please type the phrases manually.'});
        }
    </script>
</head>
<body>
<div class="container">
    <h4 class="header">Please Type the Following Phrase:</h4>
    <h5>"The quick brown fox jumps over the lazy dog"</h5>
    {% for message in get_flashed_messages() %}
    <div class="card-panel red lighten-2">{{ message }}</div>
    {% endfor %}
    <form method="POST" class="col s12" onsubmit="document.getElementById('keystrokeData').value = JSON.stringify(keystrokes);">
        <div class="row">
            {% for i in range(1, 6) %}
            <div class="input-field col s12">
                <input type="text" name="phrase{{i}}" id="phrase{{i}}" onkeydown="recordKeystroke(event, 'down');" onkeyup="recordKeystroke(event, 'up');" onpaste="preventPaste(event)" autocomplete="off" required>
                <label for="phrase{{i}}">Phrase {{i}}</label>
            </div>
            {% endfor %}
        </div>
        <input type="hidden" id="keystrokeData" name="keystrokeData">
        <button type="submit" class="waves-effect waves-light btn">Submit</button>
    </form>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</body>
</html>
""")


def save_data(email, phrases, keystroke_data):
    directory = f"./data/{email}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = os.path.join(directory, "phrases.csv")
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Phrase'])
        for phrase in phrases:
            writer.writerow([phrase])
    
    keystroke_filename = os.path.join(directory, "keystrokes.csv")
    with open(keystroke_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Key', 'Action', 'Time'])
        for keystroke in eval(keystroke_data):
            writer.writerow([keystroke['key'], keystroke['action'], keystroke['time']])

def read_durations(filename):
    durations = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Key']
            duration = float(row['Average Duration (ms)'])
            durations[key] = duration
    return durations


def calculate_average_durations(email):
    directory = f"./data/{email}"
    input_filename = os.path.join(directory, "keystrokes.csv")
    output_filename = os.path.join(directory, "average_keystroke_durations.csv")
    
    # Dictionary to store keystrokes
    keystrokes = defaultdict(list)
    
    # Read keystrokes from file
    with open(input_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Key']
            action = row['Action']
            time = int(row['Time'])
            
            if action == 'down':
                keystrokes[key].append((time, 'down'))
            elif action == 'up' and key in keystrokes:
                keystrokes[key].append((time, 'up'))

    # Calculate average durations
    durations = {}
    for key, times in keystrokes.items():
        down_times = [t[0] for t in times if t[1] == 'down']
        up_times = [t[0] for t in times if t[1] == 'up']
        paired_times = [(d, u) for d, u in zip(down_times, up_times) if u > d]  # Ensure up time is after down time
        if paired_times:
            average_duration = sum(up - down for down, up in paired_times) / len(paired_times)
            durations[key] = average_duration

    # Write the average durations to a new CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Key', 'Average Duration (ms)'])
        for key, avg_duration in durations.items():
            writer.writerow([key, float(avg_duration)])


def calculate_similarity(durations1, durations2):
    # Using Euclidean distance to calculate similarity
    keys = set(durations1.keys()).intersection(durations2.keys())
    if not keys:
        return float('inf')
    return np.sqrt(sum((durations1[key] - durations2[key])**2 for key in keys))

# Function to find the closest match...
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

if __name__ == '__main__':
    app.run(debug=True)
