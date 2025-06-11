from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/set_name', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('monitor', person=name))
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

@app.route("/data/append")
def data_append():
    try:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dist = request.args.get('dist')
        
        if not dist:
            return jsonify({"error": "Missing distance parameter"}), 400
        
        try:
            dist = float(dist)
        except ValueError:
            return jsonify({"error": "Invalid distance value"}), 400

        with open('data.txt', 'a') as f:
            f.write(f"{dt},{dist}\n")
        
        return jsonify({"message": "Data appended successfully",
                       "datetime": dt,
                       "distance": dist})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/about")
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)