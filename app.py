from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
  return render_template("index.html")


@app.route('/get_recent_data')
def get_recent_data():
    df = pd.read_csv('Data/data.csv', names=["Timestamp", "Temperature", "Humidity"], delimiter=',')
    return jsonify(df.iloc[-10:].values.tolist()), 200


@app.route('/predict_weather')
def predict_weather():
  
  # Parse data
  df = pd.read_csv('Data/data.csv', names=["Timestamp", "Temperature", "Humidity"], delimiter=',')
  df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
  df['Year'] = df['Timestamp'].dt.year
  df['Month'] = df['Timestamp'].dt.month
  df['Day'] = df['Timestamp'].dt.day
  
  # Split dataset into training and testing
  X = df[['Year', 'Month', 'Day']]
  y = df['Temperature']
  
  # Train model
  model = LinearRegression()
  model.fit(X, y)

  # Predict temperature for next day
  tomorrow: datetime = datetime.today() + timedelta(days=1)
  tomorrow_df = pd.DataFrame({'Year': [tomorrow.year], 'Month': [tomorrow.month], 'Day': [tomorrow.day]})
  next_day_temperature = model.predict(tomorrow_df)
  
  print(f"The temperature for {tomorrow.strftime('%Y-%m-%d')} will be {next_day_temperature[0]}.")
  return {"temp": next_day_temperature[0]}, 200



if __name__ == "__main__":
    app.run(debug=True)
