import requests
from flask import Flask, jsonify

app = Flask(__name__)

ORCHESTRATOR_URL = "http://localhost:8441/orchestrator"


@app.route('/motion/detect', methods=['POST'])
def detect_motion():
    query = {
        "orchestrationFlags": {
            "pingProviders": True,
            "overrideStore": True
        },
        "requestedService": {
            "serviceDefinitionRequirement": "light-control",
            "interfaceRequirements": ["HTTP-INSECURE-JSON"]
        },
        "requesterSystem": {
            "systemName": "motion-sensor-1",
            "address": "localhost",
            "port": 5001
        }
    }

    # Wyślij zapytanie do Orchestratora
    try:
        response = requests.post(f"{ORCHESTRATOR_URL}/orchestration", json=query)
        response_data = response.json()

        # Wyświetl odpowiedź debugowo
        print("Orchestrator response:", response_data)

        # Sprawdź odpowiedź
        orchestration_response = response_data.get("response")
        if orchestration_response:
            provider_info = orchestration_response[0].get("provider")
            service_uri = orchestration_response[0].get("serviceUri")

            # Wyślij zapytanie do dostawcy
            light_url = f"http://{provider_info['address']}:{provider_info['port']}{service_uri}/on"
            light_response = requests.post(light_url)
            return jsonify({"status": "Motion detected, light turned ON"}), 200

    except Exception as e:
        print("Error during orchestration:", str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "No light found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
