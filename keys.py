class WLAN_INFO:
    ssid = "WIFI_NAME"
    key = "WIFI_PASSWORD"


class MQTT:
    token = "TOKEN_KEY"
    name = "DEVICE_NAME"
    serial = "DATACAKE_SERIAL_NUMBER"
    serverURL = "mqtt.datacake.co"
    port = 1883

    def url(_fieldName):
        return "dtck-pub/DEVICE_NAME_HERE/DATACAKE_GUID_HERE/{}".format(_fieldName)
