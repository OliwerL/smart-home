# Project: Smart Home Control System

## Project Description

This project implements a smart home management system that allows for controlling lights, heating, windows, and motion detection. The project is based on REST API microservices built using Python and Flask. The system relies on the Eclipse Arrowhead platform, which enables service registration, discovery, and dynamic service management in a microservices environment.

## Features

### 1. Services:

#### Lights
- **Files:** `light_service_1.py`, `light_service_2.py`, `light_service_3.py`
- **Functions:**
  - Turn on the light (`/light/on`)
  - Turn off the light (`/light/off`)
  - Check light status (`/light/status`)

#### Thermostat
- **File:** `thermostat_service.py`
- **Functions:**
  - Turn on heating if all windows are closed (`/heating/on`)
  - Turn off heating (`/heating/off`)
  - Check heating status (`/heating/status`)

#### Window Sensors
- **Files:** `window_sensor_1.py`, `window_sensor_2.py`
- **Functions:**
  - Open window (`/window/open`)
  - Close window (`/window/close`)
  - Check window status (`/window/status`)

#### Motion Sensors
- **Files:** `motion_sensor_1.py`, `motion_sensor_2.py`, `motion_sensor_3.py`
- **Functions:**
  - Detect motion and automatically turn on the nearest light (`/motion/detect`)

### 2. Service Registration Management
- **Service Registration:** `register_services.py`
- **Service Unregistration:** `unregister_services.py`

## Architecture

The system is based on microservices that communicate with each other using HTTP. Services are registered in a service registry and can be dynamically discovered through the Orchestrator mechanism.

## Testing

Each service provides a REST API that can be tested using tools such as Postman, cURL, or a web browser. For example:

- Turn on a light:
```bash
curl -X POST http://localhost:5004/light/on
```

- Check window status:
```bash
curl -X GET http://localhost:5007/window/status
```

## File Structure

- `light_service_1.py`, `light_service_2.py`, `light_service_3.py` - Services managing lights.
- `thermostat_service.py` - Service managing the thermostat.
- `window_sensor_1.py`, `window_sensor_2.py` - Services managing window sensors.
- `motion_sensor_1.py`, `motion_sensor_2.py`, `motion_sensor_3.py` - Services managing motion sensors.
- `register_services.py` - Script for registering services in the service registry.
- `unregister_services.py` - Script for unregistering services from the service registry.
