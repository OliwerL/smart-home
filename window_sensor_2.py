import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Globalny stan okien
window_status = "CLOSED"

THERMOSTAT_URL = "http://localhost:5009/heating/window_status"

@app.route('/window/open', methods=['POST'])
def open_window():
    """Otwiera okno i informuje termostat."""
    global window_status
    window_status = "OPEN"
    requests.post(THERMOSTAT_URL, json={"window_open": True})
    return jsonify({"status": "Window opened"}), 200

@app.route('/window/close', methods=['POST'])
def close_window():
    """Zamyka okno i informuje termostat."""
    global window_status
    window_status = "CLOSED"
    requests.post(THERMOSTAT_URL, json={"window_open": False})
    return jsonify({"status": "Window closed"}), 200

@app.route('/window/status', methods=['GET'])
def get_window_status():
    """Zwraca status okna."""
    return jsonify({"window_status": window_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)  # Czujnik okna 2
