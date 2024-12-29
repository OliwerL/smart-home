import requests

SERVICE_REGISTRY_URL = "http://localhost:8443/serviceregistry/register"

def register_service(service_definition, system_name, address, port, service_uri):
    data = {
        "serviceDefinition": service_definition,
        "providerSystem": {
            "systemName": system_name,
            "address": address,
            "port": port
        },
        "serviceUri": service_uri,   # Dodajemy serviceUri
        "interfaces": ["HTTP-INSECURE-JSON"],
        "metadata": {"protocol": "HTTP"}
    }
    response = requests.post(SERVICE_REGISTRY_URL, json=data)
    print(f"Registration status for {system_name} ({service_definition}): {response.status_code}")
    print(f"Response: {response.text}")

# Rejestracja przykładowa z dopasowanym serviceUri:
register_service("motion-sensor", "motion-sensor-1", "localhost", 5001, "/motion")
register_service("motion-sensor", "motion-sensor-2", "localhost", 5002, "/motion")
register_service("motion-sensor", "motion-sensor-3", "localhost", 5003, "/motion")

register_service("light-control", "smart-light-1", "localhost", 5004, "/light")
register_service("light-control", "smart-light-2", "localhost", 5005, "/light")
register_service("light-control", "smart-light-3", "localhost", 5006, "/light")

register_service("window-sensor", "window-sensor-1", "localhost", 5007, "/window")
register_service("window-sensor", "window-sensor-2", "localhost", 5008, "/window")

register_service("thermostat-control", "thermostat-1", "localhost", 5009, "/heating")
