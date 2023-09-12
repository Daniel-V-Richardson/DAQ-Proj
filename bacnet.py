import BAC0
import json
import time

# Initialize BACnet
bacnet = BAC0.lite(ip="192.168.65.158", port=47809)

def main():
    while True:
        data = {}  # Create a new data dictionary for each iteration
        
        for x in range(1, 4):  # Analog inputs typically start from 1, not 0
            object_type = "analogInput"
            instance_id = str(x)
            property_name = "presentValue"
            address = f"{bacnet.ip} {object_type} {instance_id} {property_name}"
            
            try:
                value = bacnet.read(address)
                data[f"Analog_input{x}"] = value
            except Exception as e:
                print(f"Error reading Analog_input{x}: {e}")
        
        print(json.dumps(data, indent=2))
        time.sleep(5)

# Run main
if __name__ == '__main__':
    main()
