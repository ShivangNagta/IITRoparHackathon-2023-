from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def run_do():
    try:
        # Run the do.py script when the button is clicked
        subprocess.run(["python", "addFaces.py"], check=True)
        result = "do.py executed successfully"
    except subprocess.CalledProcessError as e:
        result = f"Error executing addFaces.py: {e}"

    return result

if __name__ == '_main_':
    app.run()