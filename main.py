import datetime
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/health")
def health():
   
    return "<p>Server is up and running.</p>"

@app.route("/monitor")
def monitor():

    # calculate some metrics here
    data = []

    with open('data.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                datetime, temperature = parts
                data.append({'datetime': datetime, 'temperature': float(temperature)})

    person = "Pepe"
   
    return render_template('monitor.html', data=data, person=person)

@app.route("/data/append")
def data_append():

    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = request.args.get('temp')
    if not dt:
        return "<p>Error: Missing parameters</p>", 400
    
    # Here you would typically append the data to a database or a file
    print(f"Appending data: datetime={dt}, temp={temp}")

    with open('data.txt', 'a') as f:
        f.write(f"{dt},{temp}\n")

    return "<p>Data appended successfully.</p>"