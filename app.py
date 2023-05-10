from flask import Flask, render_template, jsonify
from flask_cors import CORS
import numpy as np
import csv
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
  return render_template("index.html")


@app.route('/get_recent_data')
def get_recent_data():
    data = []
    with open('Data/data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    data = data[-10:]
    return jsonify(data), 200



@app.route('/predict_weather')
def predict_weather():
    data = []
    with open('Data/data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            data.append([timestamp.year, timestamp.month, timestamp.day, float(row[1])])
    data = np.array(data)
    X = data[:, :3]
    y = data[:, 3]
    
    model = LinearRegression()
    model.fit(X, y)

    tomorrow = datetime.today() + timedelta(days=1)
    next_day_temperature = model.predict(np.array([[tomorrow.year, tomorrow.month, tomorrow.day]]))
  
    print(f"The temperature for {tomorrow.strftime('%Y-%m-%d')} will be {next_day_temperature[0]}.")
    return {"temp": next_day_temperature[0]}, 200



if __name__ == "__main__":
    app.run(debug=True)
