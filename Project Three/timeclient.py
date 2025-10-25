# Madison Neiswonger
# CS 372
# 10/25/25
# Project Three: Atomic Time Section

import socket
import time

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

def get_nist_time():
    try:
# Connecting to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(("time.nist.gov", 37))

# Receive the data
            data = s.recv(4)

    except Exception:
        return None

# Decode the Data
    if len(data) < 4:
        return None

    return int.from_bytes(data, byteorder="big")

if __name__ == "__main__":
    nist_time = get_nist_time()
    print(f"NIST time: {nist_time}")
    print(f"System time: {system_seconds_since_1900()}")