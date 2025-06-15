from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/set_name', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        try:
            name = request.form['name']
            print(f"Name received: {name}")  # Debugging line
            return redirect(url_for('monitor', person=name))
        except Exception as e:
            print(f"Error in set_name: {e}")
            return "An error occurred in set_name", 500
    return render_template('set_name.html')

@app.route("/monitor")
def monitor():
    person = request.args.get('person', "Cinthya")  # Default name is Cinthya
    data = []

    try:
        with open('data.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    dt, distance = parts
                    data.append({
                        'datetime': dt,
                        'distance': float(distance)
                    })
    except FileNotFoundError:
        data = []

    # Limit to last 10 entries
    data = data[-10:]
    return render_template('monitor.html', data=data, person=person)

@app.route("/data/append", methods=['GET'])
def data_append():
    dist = request.args.get('dist')
    if dist is None:
        # Show the form if no distance is provided
        return render_template('data_append.html')
    try:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dist_val = float(dist)
        with open('data.txt', 'a') as f:
            f.write(f"{dt},{dist_val}\n")
        return render_template('data_append.html', message="Data appended successfully!")
    except ValueError:
        return render_template('data_append.html', message="Invalid distance value!")
    except Exception as e:
        return render_template('data_append.html', message=f"Error: {e}")

@app.route("/about")
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
