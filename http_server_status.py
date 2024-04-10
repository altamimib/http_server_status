import requests
import time
from prometheus_client import start_http_server, Gauge
from datetime import datetime

# Create a Gauge metric for the API check
api_status = Gauge('web_api_status', 'Status of the web API (1 for up, 0 for down)')

def check_api():
    url = "https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        api_status.set(1)  # Set metric to 1 for success
        print(f"[{datetime.now()}] API check successful.")
    except requests.exceptions.RequestException as e:
        api_status.set(0)  # Set metric to 0 for failure
        print(f"[{datetime.now()}] Error checking API: {e}")
        

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8765 (choose a suitable port)
    start_http_server(8765)

    while True:
        check_api()
        time.sleep(30)  # Check every 30 seconds
