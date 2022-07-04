import time
import pycom
import machine
import network

from network import WLAN
from mqtt import MQTTClient
from keys import *

# =================== VARIABLES ===================

# Conversion from ANALOG pin data to digital variables
analogToDigital = machine.ADC()

# MCP9700
tempPin = analogToDigital.channel(pin='P13')
millivoltsAtZero = 500.0

class Status:
    COLD = "Cold"
    HEAT_UP = "Heating up"
    HEAT_DOWN = "Cooling down"
    HOT = "Hot"

tempThresholdLow = 30
tempThresholdHigh = 35

oldSensorData = {
    "TEMPERATURE": 0.0,
    "STATUS": Status.COLD,
    "TIME": 0,
    "SEND_NOTIFICATION": False
}

sensorData = {
    "TEMPERATURE": 0.0,
    "STATUS": Status.COLD,
    "TIME": 0,
    "SEND_NOTIFICATION": False
}

sensorData_NOPUB = {
    "TIME_START": 0, # Timestamp for first detecting Status.HOT
    "TIME_MAX": 300, # Seconds
    "TIME_LAST_NOTIFICATION": 0,
    "STATUS_TICKS": 0,
    "STATUS_TICK_MAX": 5
}

# Time to wait for updating server
minutes = 15
seconds = 0

sendCooldown = (minutes * 60) + seconds # Seconds between sending data to server
lastSentData = 0 # Timestamp for last sending data to server
secondsToSleep = 5 # Seconds between each loop

# =================== BOOT START ===================
print("")

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

print('Enabling WLAN...', end='')
wlan = WLAN()
pycom.wifi_mode_on_boot(WLAN.STA)
if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
print(' DONE')
time.sleep(2)

if not wlan.isconnected():
    print("Connecting to WLAN... ", end='\r')
    symbols = ['-', '\\', '|', '/']
    wlan.connect(WLAN_INFO.ssid, auth=(network.WLAN.WPA2, WLAN_INFO.key))

    symbolIdx = 0
    while not wlan.isconnected():
        if not symbolIdx < len(symbols) - 1:
            symbolIdx = 0
        symbol = symbols[symbolIdx]
        print("Connecting to WLAN... {}".format(symbol), end='\r')
        time.sleep_ms(50)
        symbolIdx = symbolIdx + 1
    print('Connecting to WLAN... DONE')
print('Connected to WLAN:', wlan.ifconfig())

# MQTT Client
print('Connecting to MQTT server...', end='')
client = MQTTClient(MQTT.serial, MQTT.serverURL, MQTT.port, MQTT.token, MQTT.token)

if client.connect() == 0:
    print(' DONE')
else:
    print(' FAILED')
    exit(-1)

# =================== FUNCTION TABLE ===================
def readTemp():
    millivolts = tempPin.voltage()
    celsius = (millivolts - millivoltsAtZero) * 0.1
    sensorData['TEMPERATURE'] = celsius

def determineStatusAndTime():
    celsius = sensorData['TEMPERATURE']

    # LOW
    if celsius < tempThresholdLow:
        sensorData["STATUS"] = Status.COLD
        sensorData["TIME"] = 0

    # MIDDLE
    elif celsius < tempThresholdHigh:
        if sensorData["STATUS"] == Status.HOT:
            sensorData["STATUS"] = Status.HEAT_DOWN
        elif sensorData["STATUS"] == Status.COLD:
            sensorData["STATUS"] = Status.HEAT_UP

    # HIGH
    else:
        # Was already hot
        if (sensorData["STATUS"] == Status.HOT):
            # Time since last
            now = time.time()
            span = now - sensorData_NOPUB['TIME_START']
            sensorData["TIME"] = span

        # Just got hot
        else:
            sensorData["STATUS"] = Status.HOT
            now = time.time()
            sensorData_NOPUB['TIME_START'] = now
            sensorData_NOPUB['TIME_LAST_NOTIFICATION'] = now # To not send notification instantly!

def publish(field):
    print("\tPublishing '{}'...".format(field), end='')
    client.publish(MQTT.url(field), str(sensorData[field]))
    print(' DONE')
    oldSensorData[field] = sensorData[field]

def publishSensorData():
    print("Sending to DATABASE...")
    for field in sensorData:
        if field == 'TEMPERATURE' or sensorData[field] != oldSensorData[field]: # Always update temperature and only update changes for the others.
            publish(field)
        else:
            print('\t{} has not changed.'.format(field))
    print('Publish complete.')

def updateSensorData():
    print('Reading sensors...', end='')
    readTemp()
    determineStatusAndTime()

    # If status is outdated, inctease the status ticks
    if (oldSensorData['STATUS'] != sensorData['STATUS']):
        sensorData_NOPUB['STATUS_TICKS'] = sensorData_NOPUB['STATUS_TICKS'] + 1
    # Else reset the status ticks
    else:
        sensorData_NOPUB['STATUS_TICKS'] = 0
    print(' DONE')

def doNotificationLogic():
    forcedPublish = False
    sendDisable = False

    # If status is HOT, handle notification logic
    if sensorData['STATUS'] == Status.HOT:
        # If time exceeded, forceds publish is sent, and a notificaion to grab coffee is sent.
        if span > sensorData_NOPUB['TIME_MAX']:
            forcedPublish = True
            sensorData['SEND_NOTIFICATION'] = True
            sensorData_NOPUB['TIME_LAST_NOTIFICATION'] = now # Reset the publishing timer

    # If status ticks exceed the limit, publishing is forced no matter the timer.
    if sensorData_NOPUB['STATUS_TICKS'] >= sensorData_NOPUB['STATUS_TICK_MAX']:
        forcedPublish = True

    # Check if just sent notification
    if oldSensorData['SEND_NOTIFICATION']:
        # Reset SEND_NOTIFICATION on Datacake database. This will also allow for next timer pulse to notify discord.
        sensorData['SEND_NOTIFICATION'] = False
        sendDisable = True

    return forcedPublish, sendDisable

# =================== PROGRAM START ===================

pycom.rgbled(0x00FF00) # GREEN

while True:
    now = time.time()
    span = now - sensorData_NOPUB['TIME_LAST_NOTIFICATION']

    updateSensorData()
    print(sensorData, sensorData_NOPUB)

    forcedPublish, sendDisable = doNotificationLogic()

    # This will reset the online database variable with a value of False
    if sendDisable:
        publish('SEND_NOTIFICATION')

    # If the time since last publish is exceeded, publish update
    if forcedPublish or now - lastSentData > sendCooldown:
        publishSensorData()
        lastSentData = now

    # Sleep
    for i in range(secondsToSleep, 0, -1):
        print('Sleeping... ({seconds}s)  '.format(seconds = i), end='\r')
        time.sleep(1)
