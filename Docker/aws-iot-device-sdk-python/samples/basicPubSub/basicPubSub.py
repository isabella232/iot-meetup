'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import datetime
from pyspectator.processor import Cpu
from time import sleep
cpu = Cpu(monitoring_latency=1)

awaitingResponse = False

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    global awaitingResponse
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    # If the message did not come from our own, we set the awaitResponse flag
    if (message.topic != subscribeTopic + '/' + clientId):
        awaitingResponse = True

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-s", "--subscribetopic", action="store", dest="subscribeTopic", default="room/public/", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic
subscribeTopic = args.subscribeTopic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(subscribeTopic + '/+', 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:

    # If we are awaiting a response, the means we got a message, return some useless result.
    if awaitingResponse:
        awaitingResponse = False
        message = {}

        returnSelector = int(time.time()) % 15
        if returnSelector == 1:
            message['message'] = "What do you mean?"
        elif returnSelector == 2:
            message['message'] = "Don't think I understand what you mean"
        elif returnSelector == 3:
            message['message'] = "Could you repeat that question?"
        elif returnSelector == 4:
            message['message'] = "Machine says YeS!"
        elif returnSelector == 5:
            message['message'] = "Can you ask this to someone else? I have no idea"
        elif returnSelector == 6:
            message['message'] = "At your service"
        elif returnSelector == 7:
            message['message'] = "The Moon is an astronomical body that orbits planet Earth and is Earth's only permanent natural satellite. "
        elif returnSelector == 8:
            message['message'] = "I cannot make any cat sounds"
        elif returnSelector == 9:
            message['message'] = "Are you sure?"
        elif returnSelector == 10:
            message['message'] = "The Sind sparrow (Passer pyrrhonotus) is a bird of the sparrow family, Passeridae, found around the Indus valley region in South Asia. "
        elif returnSelector == 11:
            message['message'] = "Mmmmm..."
        elif returnSelector == 12:
            message['message'] = "Don't think that is possible"
        elif returnSelector == 13:
            message['message'] = "Computer software, or simply software, is a generic term that refers to a collection of data or computer instructions that tell the computer how to work, in contrast to the physical hardware from which the system is built, that actually performs the work"
        else:
            message['message'] = "yeah, sure!"

        message['sequence'] = loopCount
        messageJson = json.dumps(message)

        # Publish to the topic
        myAWSIoTMQTTClient.publish(subscribeTopic + '/' + clientId, messageJson, 1)

        # Log this
        print('Published topic %s: %s' % (subscribeTopic + '/' + clientId, messageJson))

    if ((loopCount % 10) == 0) and loopCount < 1000:
        if args.mode == 'both' or args.mode == 'publish':
            # Send our CPU usage
            message = {}
            message['message'] = str(datetime.datetime.now()) + ": The CPU load of client " + clientId + " is " + str(cpu.load)
            message['sequence'] = loopCount
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            
            print('Published topic %s: %s' % (topic, messageJson))

    loopCount +=1
    time.sleep(1)


