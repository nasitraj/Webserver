from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup function
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id TEXT,
                    temperature REAL,
                    humidity REAL,
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_sensor_data(sensor_id, temperature, humidity):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''INSERT INTO sensor_readings (sensor_id, temperature, humidity, timestamp)
                 VALUES (?, ?, ?, ?)''', (sensor_id, temperature, humidity, timestamp))
    conn.commit()
    conn.close()

# Endpoint to fetch sensor data
@app.route('/sensor_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

# Endpoint to manually add sensor data to the database
@app.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    # Getting data from request JSON
    sensors = request.json();
    sensor_id = request.json.get('sensor_id')
    temperature = request.json.get('temperature')
    humidity = request.json.get('humidity')

    if sensor_id is None or temperature is None or humidity is None:
        return jsonify({'error': 'Missing data in request'}), 400

    # Insert data into the database
    insert_sensor_data(sensor_id, temperature, humidity)

    return jsonify({
        'message': 'Sensor data added successfully',
        'sensor_id': sensor_id,
        'temperature': temperature,
        'humidity': humidity
    }), 201

if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Run the Flask app
    app.run(debug=True)
