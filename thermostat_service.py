import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Globalny stan ogrzewania i temperatura
heating_state = "OFF"
temperature = 20.0  # Początkowa temperatura w stopniach Celsjusza

# URL Orchestratora
ORCHESTRATOR_URL = "http://localhost:8441/orchestrator"


@app.route('/heating/window_status', methods=['POST'])
def update_window_status():
    """Aktualizuje temperaturę, jeśli okno zostało otwarte."""
    global temperature, heating_state
    window_open = request.json.get("window_open", False)

    if window_open:
        temperature -= 1.0  # Obniż temperaturę o 1 stopień
        heating_state = "OFF"  # <-- automatycznie WYŁĄCZ ogrzewanie, gdy okno jest otwarte
        print("Okno otwarte – wyłączam ogrzewanie")
    else:
        temperature += 0.5  # Podnoś temperaturę (lub po prostu nie zmieniaj)
        heating_state = "ON"  # <-- automatycznie WŁĄCZ ogrzewanie, gdy okno jest zamknięte
        print("Okno zamknięte – włączam ogrzewanie")

    return jsonify({
        "status": "Temperature updated",
        "heating_state": heating_state,
        "temperature": temperature
    }), 200


@app.route('/heating/on', methods=['POST'])
def turn_on_heating():
    """Włącza ogrzewanie, jeśli okna są zamknięte."""
    query = {
        "orchestrationFlags": {
            "pingProviders": True,
            "overrideStore": True
        },
        "requestedService": {
            "serviceDefinitionRequirement": "window-sensor",
            "interfaceRequirements": ["HTTP-INSECURE-JSON"]
        },
        "requesterSystem": {
            "systemName": "thermostat-1",
            "address": "localhost",
            "port": 5009
        }
    }

    try:
        # Wysłanie zapytania do Orchestratora
        response = requests.post(f"{ORCHESTRATOR_URL}/orchestration", json=query)
        response_data = response.json()

        print("Orchestrator response:", response_data)

        # Sprawdzenie odpowiedzi
        orchestration_response = response_data.get("response")
        if orchestration_response:
            for provider in orchestration_response:
                provider_info = provider.get("provider")
                service_uri = provider.get("serviceUri")

                # Pobierz status okna
                window_status_url = f"http://{provider_info['address']}:{provider_info['port']}{service_uri}/status"
                status_response = requests.get(window_status_url)
                if status_response.status_code == 200:
                    window_status = status_response.json().get("window_status")
                    if window_status == "OPEN":
                        return jsonify({"error": "Cannot turn ON heating, window is OPEN"}), 403

            # Jeśli wszystkie okna są zamknięte, włącz ogrzewanie
            global heating_state
            heating_state = "ON"
            return jsonify({"status": "Heating turned ON"}), 200

    except Exception as e:
        print("Error during orchestration:", str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "No window-sensor services found"}), 404

@app.route('/heating/off', methods=['POST'])
def turn_off_heating():
    """Wyłącza ogrzewanie."""
    global heating_state
    heating_state = "OFF"
    return jsonify({"status": "Heating turned OFF"}), 200

@app.route('/heating/status', methods=['GET'])
def heating_status():
    """Sprawdza aktualny stan ogrzewania i temperaturę."""
    return jsonify({"heating_state": heating_state, "temperature": temperature}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)  # Port dla termostatu
