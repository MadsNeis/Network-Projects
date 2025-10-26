# Madison Neiswonger
# CS 372
# 10/26/25
# Project Four: Validating a TCP Packet

import os

# Dots and numbers ip address to bytestrings
def convertIP_to_bytes(ip_str: str) -> bytes:
    parts = [int(p) for p in ip_str.strip().split(".")]
    return b"".join(p.to_bytes(1, "big") for p in parts)

def compute_tcp_checksum(pseudo_header: bytes, tcp_0_checksum: bytes) -> int:
    data = pseudo_header + tcp_0_checksum
    if len(data) % 2 == 1:
        data += b'\x00'
    total = 0
    for i in range(0, len(data), 2):
        word = int.from_bytes(data[i:i+2], 'big')
        total += word
        total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff

results = []

for i in range(10):
    addr_name = f"tcp_addrs_{i}.txt"
    data_name = f"tcp_data_{i}.dat"

# Read addr file
    with open(addr_name, "r") as f:
        src_ip, dst_ip = f.read().strip().split()
    src_bytes = convertIP_to_bytes(src_ip)
    dst_bytes = convertIP_to_bytes(dst_ip)

# Read data file
    with open(data_name, "rb") as f:
        tcp_data = f.read()

# TCP data length
    tcp_len = len(tcp_data)

# PseudoHeader
    pseudo = src_bytes + dst_bytes + b'\x00' + b'\x06' + tcp_len.to_bytes(2, "big")
# Original Checksum
    original_checksum = int.from_bytes(tcp_data[16:18], "big")
    tcp_zero = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
    calculated_checksum = compute_tcp_checksum(pseudo, tcp_zero)
    verdict = "PASS" if calculated_checksum == original_checksum else "FAIL"
    results.append((i, verdict, original_checksum, calculated_checksum))


for item in results:
    if item[1] in ("PASS", "FAIL"):
        _, verdict, orig, calc = item
        print(verdict)
    else:
        print(item[1])
