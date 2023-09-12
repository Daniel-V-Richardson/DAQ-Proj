import socket

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

ip = "192.168.65.158"  # Replace with your IP address
if is_valid_ip(ip):
    print("Valid IP address")
else:
    print("Invalid IP address")
