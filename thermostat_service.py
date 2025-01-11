import threading
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Globalny stan ogrzewania i temperatura
heating_state = "OFF"
temperature = 20.0  # Początkowa temperatura w stopniach Celsjusza
target_temperature = 22.0  # Docelowa temperatura
min_temperature = 17.0  # Minimalna temperatura przy otwartym oknie
window_open = False  # Stan okna
temperature_lock = threading.Lock()  # Blokada dla zmiennej temperatury


def manage_temperature():
    """Wątek zarządzający temperaturą w systemie."""
    global temperature, heating_state, window_open

    while True:
        time.sleep(5)  # Czas aktualizacji temperatury
        with temperature_lock:
            if window_open:
                if temperature > min_temperature:
                    temperature -= 0.5  # Obniżaj temperaturę co 5 sekund
            elif heating_state == "ON":
                if temperature < target_temperature:
                    temperature += 0.5  # Podnoś temperaturę co 5 sekund
                else:
                    heating_state = "OFF"  # Wyłącz ogrzewanie, gdy osiągnięto docelową temperaturę


@app.route('/heating/window_status', methods=['POST'])
def update_window_status():
    """Aktualizuje stan okna i wyłącza ogrzewanie, jeśli okno jest otwarte."""
    global window_open, heating_state

    window_open = request.json.get("window_open", False)

    with temperature_lock:
        if window_open:
            heating_state = "OFF"  # Wyłącz ogrzewanie, gdy okno jest otwarte
            print("Okno otwarte – wyłączam ogrzewanie")
        else:
            print("Okno zamknięte – kontrola ogrzewania przywrócona")

    return jsonify({
        "status": "Window status updated",
        "window_open": window_open,
        "heating_state": heating_state,
        "temperature": temperature
    }), 200


@app.route('/heating/on', methods=['POST'])
def turn_on_heating():
    """Włącza ogrzewanie, jeśli okna są zamknięte."""
    global heating_state

    with temperature_lock:
        if not window_open and temperature < target_temperature:
            heating_state = "ON"
            return jsonify({"status": "Heating turned ON"}), 200
        elif window_open:
            return jsonify({"error": "Cannot turn ON heating, window is OPEN"}), 403
        else:
            return jsonify({"status": "Heating is already at target temperature"}), 200


@app.route('/heating/off', methods=['POST'])
def turn_off_heating():
    """Wyłącza ogrzewanie."""
    global heating_state

    with temperature_lock:
        heating_state = "OFF"

    return jsonify({"status": "Heating turned OFF"}), 200


@app.route('/heating/status', methods=['GET'])
def heating_status():
    """Sprawdza aktualny stan ogrzewania i temperaturę."""
    with temperature_lock:
        return jsonify({
            "heating_state": heating_state,
            "temperature": temperature,
            "target_temperature": target_temperature,
            "window_open": window_open
        }), 200


if __name__ == '__main__':
    # Uruchomienie wątku zarządzającego temperaturą
    temperature_thread = threading.Thread(target=manage_temperature, daemon=True)
    temperature_thread.start()

    # Uruchomienie aplikacji Flask
    app.run(host='0.0.0.0', port=5009)
