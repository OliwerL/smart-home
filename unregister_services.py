import requests

SERVICE_MGMT_URL = "http://localhost:8443/serviceregistry/mgmt"

def get_service_id(system_name, address, port):
    # Pobierz ID usługi na podstawie parametrów
    response = requests.get(SERVICE_MGMT_URL)
    if response.status_code == 200:
        services = response.json().get("data", [])
        for service in services:
            provider = service.get("provider", {})
            if provider.get("systemName") == system_name and provider.get("address") == address and provider.get("port") == port:
                return service.get("id")
    return None

def unregister_service_by_id(service_id):
    if service_id is not None:
        url = f"{SERVICE_MGMT_URL}/{service_id}"
        response = requests.delete(url)
        print(f"Unregistration status for service ID {service_id}: {response.status_code}")
        print(f"Response: {response.text}")
    else:
        print(f"Service ID not found. Cannot unregister.")

# Wyrejestruj przykłady
services_to_unregister = [
    ("motion-sensor-1", "localhost", 5001),
    ("motion-sensor-2", "localhost", 5002),
    ("motion-sensor-3", "localhost", 5003),
    ("smart-light-1", "localhost", 5004),
    ("smart-light-2", "localhost", 5005),
    ("smart-light-3", "localhost", 5006),
    ("window-sensor-1", "localhost", 5007),
    ("window-sensor-2", "localhost", 5008),
    ("thermostat-1", "localhost", 5009),
]

for system_name, address, port in services_to_unregister:
    service_id = get_service_id(system_name, address, port)
    unregister_service_by_id(service_id)
