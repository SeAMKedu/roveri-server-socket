import re
import socket

import colorama
colorama.init()

# Server address information.
HOST = "192.168.0.100"
PORT = 3000

ADDR_ABB = "192.168.0.105"
ADDR_UR5 = "192.168.0.106"
ADDR_TB4 = "192.168.0.101"

# Colors.
COLOR_ERR = f"{colorama.Style.BRIGHT}{colorama.Fore.RED}"
COLOR_ABB = f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
COLOR_UR5 = f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}"
COLOR_TB4 = f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}"
COLOR_RES = colorama.Style.RESET_ALL

PATTERN1 = "getState,abb|ur5|tb4"
PATTERN2 = "setState,abb,waiting|working|ready"
PATTERN3 = "setState,ur5,waiting|working|ready"
PATTERN4 = "setState,tb4,docked|moving|onABB,onUR5"

# Commands.
GET_STATE = "getState"
SET_STATE = "setState"

# Device names.
DEVICE_ABB = "abb"
DEVICE_UR5 = "ur5"
DEVICE_TB4 = "tb4"

# States.
DOCKED = "docked"
MOVING = "moving"
READY = "ready"
ON_ABB = "onABB"
ON_UR5 = "onUR5"
WAITING = "waiting"
WORKING = "working"

# Responses.
RESPONSE_OK = "ok"
RESPONSE_NOT_OK = "notOk"

state_abb = WAITING
state_ur5 = WAITING
state_tb4 = MOVING


def create_server_socket(host: str, port: int) -> socket.socket:
    """Create a TCP/IP socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"Server socket is listening on {host}:{port}")
    return s


def validate_request(message: str) -> bool:
    """Return True if the request message is valid, False otherwise."""
    isvalid = False
    for pattern in (PATTERN1, PATTERN2, PATTERN3, PATTERN4):
        ismatch = re.search(pattern, message)
        if ismatch:
            isvalid = True
            break
    return isvalid


def set_color(address: tuple) -> str:
    color = ""
    addr = address[0]
    if addr == ADDR_ABB:
        color = COLOR_ABB
    elif addr == ADDR_UR5:
        color = COLOR_UR5
    elif addr == ADDR_TB4:
        color = COLOR_TB4
    return color


def handle_request(command: str, device: str, state: str) -> str:
    global state_abb, state_ur5, state_tb4
    response = RESPONSE_NOT_OK
    if command == GET_STATE:
        if device == DEVICE_ABB:
            response = state_abb
        elif device == DEVICE_UR5:
            response = state_ur5
        elif device == DEVICE_TB4:
            response = state_tb4
    elif command == SET_STATE:
        if device == DEVICE_ABB:
            state_abb = state
            response = RESPONSE_OK
        elif device == DEVICE_UR5:
            state_ur5 = state
            response = RESPONSE_OK
        elif device == DEVICE_TB4:
            state_tb4 = state
            response = RESPONSE_OK
    return response


def main():
    server = create_server_socket(HOST, PORT)

    while True:
        try:
            # Receive a request.
            client, address = server.accept()
            request = client.recv(128).decode()
            #print(f"New connection from {address}, message: {request}")
            # Expected request formats:
            # "getState,myDeviceName"
            # "setState,myDeviceName,myState"
            isvalid = validate_request(request)

            if isvalid == False:
                color = COLOR_ERR
                response = RESPONSE_NOT_OK
                client.sendall(response.encode())
                print(f"{color}{request} >> {response}{COLOR_RES}")
                continue

            # Handle requests.
            color = set_color(address)
            items = request.split(",")
            command = items[0]
            device = items[1]
            state = items[2] if len(items) == 3 else ""
            response = handle_request(command, device, state)

            # Send the response.
            client.sendall(response.encode())
            client.close()
            print(f"{color}{request} >> {response}{COLOR_RES}")
        except socket.error:
            pass
        except KeyboardInterrupt:
            break

    server.close()


if __name__ == "__main__":
    main()
