# Keystroke Dynamics Analysis

This Flask application captures and analyzes keystroke dynamics to identify and authenticate users based on their typing patterns. It utilizes the phrase "The quick brown fox jumps over the lazy dog" to capture comprehensive keystroke data across the alphabet.

## Project Description

This project leverages Flask, JavaScript, and advanced data processing techniques to measure and analyze the timing of keystrokes. Users are prompted to type a specific phrase, and the application captures the duration between key presses and releases. This data is then used to generate user-specific keystroke profiles, which can be compared to identify or verify users based on their unique typing patterns.

### Features

- Real-time keystroke capturing.
- Analysis of key press durations.
- User authentication based on keystroke dynamics.
- Comparison of current session data with historical data to find the closest match.

## Installation

To get this project up and running on your local machine, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/chowdary12345/keystroke.git

2. **Set up a Python Virtual Environment (Optional but recommended)**
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. **Run the Application**
flask run

## Usage
Once the application is running, navigate to http://127.0.0.1:5000/ in your web browser. Follow the on-screen instructions to enter your email and type the phrase as instructed. The system will analyze your keystrokes and provide feedback based on the analysis.

