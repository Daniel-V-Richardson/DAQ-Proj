from flask import Flask, render_template, request, jsonify
import BAC0
import logging
import time
import requests

app = Flask(__name__)
bacnet = None
mqtt_config = None


@app.route('/')
def index():
    return render_template('index.html')


def configure_mqtt(mqtt_ip, mqtt_port):
    global mqtt_client
    # mqtt_client.username_pw_set(username, password)
    mqtt_client.connect(mqtt_ip, mqtt_port)
    mqtt_client.loop_start()
    # mqtt_client.subscribe(any/topic")
    return "MQTT configured successfully."


@app.route('/configure_mqtt', methods=['POST'])
def configure_mqtt_route():
    global mqtt_config
    if not mqtt_config:
        try:
            mqtt_ip = request.form['mqtt_ip']
            mqtt_port = int(request.form['mqtt_port'])
            message = configure_mqtt(mqtt_ip, mqtt_port)
        except Exception as e:
            message = f"Error configuring MQTT: {str(e)}"
    else:
        message = "MQTT is already configured."

    return jsonify({"message": message})


rest_config = {
    "rest_url": None,
    "rest_method": None,
}


@app.route("/configure_rest", methods=["POST"])
def configure_rest():
    global rest_config

    try:
        data = request.form
        rest_url = data.get("rest_url")
        rest_method = data.get("rest_method")

        rest_config["rest_url"] = rest_url
        rest_config["rest_method"] = rest_method

        response_data = {
            "message": "REST configuration saved successfully.",
        }
        response = jsonify(response_data)
        response.headers["Custom-Header"] = "CustomHeaders"

        return response, 200

    except Exception as e:
        error_message = "Error configuring REST: " + str(e)
        return jsonify({"error": error_message}), 500


@app.route('/configure_bacnet', methods=['POST'])
def configure_bacnet():
    global bacnet
    if not bacnet:
        try:
            ip = request.form['ip']
            port = int(request.form['port'])
            bacnet = BAC0.lite(ip=ip, port=port)
            message = "BACnet configured successfully."
        except Exception as e:
            message = f"Error configuring BACnet: {str(e)}"
    else:
        message = "BACnet is already configured."

    return jsonify({"message": message})


@app.route('/get_bacnet_logs')
def get_bacnet_logs():
    global bacnet
    if bacnet:
        try:
            logs = bacnet.get_logs()
            return jsonify(logs)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "BACnet is not configured. Configure it first."})


BACNET_IP = "192.168.0.100"
# BACNET_PORT = 47809


def read_bacnet_data():
    global bacnet
    if bacnet:
        try:
            data = {}
            for x in range(0, 3):
                id = str(x)
                value = bacnet.read(
                    f"{BACNET_IP}:53522 analogInput {id} presentValue")
                value = str(value)
                data["Analog_input" + id] = value

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "BACnet is not configured. Configure it first."})


@app.route('/read_bacnet_data')
def read_bacnet_data_endpoint():
    return read_bacnet_data()


opac_config = {
    "opac_server": None,
    "opac_username": None,
    "opac_password": None,
}
data = {
    "username": None,
    "password": None,
}


@app.route("/configure_opac", methods=["POST"])
def configure_opac():
    global opac_config

    try:
        data = request.form
        opac_server = data.get("opac_server")
        opac_username = data.get("opac_username")
        opac_password = data.get("opac_password")
        opac_config["opac_server"] = opac_server
        opac_config["opac_username"] = opac_username
        opac_config["opac_password"] = opac_password
        response = requests.post(opac_server + "/configure", data=data)
        if response.status_code == 200:
            response_data = {
                "message": "OPAC Configured successfully.",
            }
        else:
            print("Error configuring OPAC:",
                  response.status_code, response.text)
            response_data = {
                "message": "Error configuring OPAC."+response.status_code + "," + response.text,
            }
        return jsonify(response_data), 200
    except Exception as e:
        error_message = "Error configuring OPAC: " + str(e)
        return jsonify({"error": error_message}), 500


if __name__ == '__main__':
    app.run(debug=True)
