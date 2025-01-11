import threading
import time
from flask import Flask, request

app = Flask(__name__)
light_state = "OFF"
light_timer = None  # Timer kontrolujący wyłączanie światła
light_timer_lock = threading.Lock()  # Blokada dla dostępu do light_timer
stop_flag = threading.Event()  # Flaga do zatrzymywania starego timera


def turn_off_light_after_delay(delay):
    """Funkcja wyłączająca światło po opóźnieniu."""
    global light_state
    if not stop_flag.wait(delay):  # Czeka przez określony czas, ale przerywa, jeśli flaga zostanie ustawiona
        with light_timer_lock:  # Zapewnia bezpieczny dostęp do zmiennej
            if light_state == "ON":  # Jeśli światło nadal jest włączone, wyłącz je
                light_state = "OFF"
                print("Light turned OFF automatically after delay")


@app.route('/light/on', methods=['POST'])
def turn_on_light():
    global light_state, light_timer, stop_flag

    # Włącz światło
    light_state = "ON"

    # Jeśli istnieje wcześniejszy timer, zatrzymaj go
    with light_timer_lock:
        if light_timer and light_timer.is_alive():
            stop_flag.set()  # Ustaw flagę, aby zatrzymać stary timer
            light_timer.join()  # Poczekaj, aż wątek się zakończy

        # Resetuj flagę i uruchom nowy timer
        stop_flag = threading.Event()
        light_timer = threading.Thread(target=turn_off_light_after_delay, args=(10,))
        light_timer.start()

    return {"status": "Light turned ON"}, 200


@app.route('/light/off', methods=['POST'])
def turn_off_light():
    global light_state, light_timer, stop_flag

    # Wyłącz światło ręcznie
    light_state = "OFF"

    # Jeśli istnieje wcześniejszy timer, zatrzymaj go
    with light_timer_lock:
        if light_timer and light_timer.is_alive():
            stop_flag.set()  # Ustaw flagę, aby zatrzymać stary timer
            light_timer.join()  # Poczekaj, aż wątek się zakończy

    return {"status": "Light turned OFF"}, 200


@app.route('/light/status', methods=['GET'])
def get_light_status():
    return {"light_state": light_state}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)  # Port dla pierwszego światła
