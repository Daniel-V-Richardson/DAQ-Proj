import BAC0
import json
import time
bacnet = BAC0.lite(ip="192.168.0.100/28", port=47809)
data = {}


def main():
    while True:
        # Reading 3 Objects from the Bacnet Simulator
        for x in range(0, 3):
            id = str(x)
        # Connect to the BACnet simulator using the IP address and port number
            value = bacnet.read(
                "192.168.0.100:53522 analogInput "+id+" presentValue")
            value = str(value)
            data["Analog_input"+id] = value

        print(json.dumps(data, indent=2))
        time.sleep(5)

#RUN main
if __name__ == '__main__':
    main()