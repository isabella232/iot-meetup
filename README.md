# Merapar Iot-Meetup

This repository contains all code files used in the Merapar IoT hands-on Meetup.

## Chat Application
It contains (a slightly modified version of) the AWS IoT Chat application see [https://github.com/aws-samples/aws-iot-chat-example](https://github.com/aws-samples/aws-iot-chat-example).  
The Chat Application uses Cognito identities to authenticate and assume rights to interact with the IoT broker.

For more details see [ReadMe](/ChatApp/aws-iot-chat-example/README.md)


## IoT Docker Container
This uses the AWS IoT Python SDK with a modified sample to interact with above chat application when connected to the same IoT Broker.  
The Docker container should be provisioned with X.509 certificate in order to allow interaction with the IoT broker.

For more details see [ReadMe](/Docker/README.md)
