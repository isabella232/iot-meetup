# Merapar AWS IoT Docker Example

This is a simple container wrapper for the AWS IoT Python SDK.

### Docker file
The DockerFile copies the aws-iot-device-sdk-python and embeds the AWS Root Certificate / startup script.

During startup, the following parameters need to be provided:

- A volume which contains a directory with the X.509 certificates (download from the AWS Console)
- CERTIFICATE -> The name of the certificate,for example 1234-certificate.pem.crt
- PRIVATE_KEY -> The name of the private key, for example 1234-private.pem.key
- THING_NAME ->  The name of the thing to be created
- IOT_ENDPOINT -> The IoT endpoint.

The docker run command could look like the following: 
```
docker run -v "/tmp/certificates":/tmp \
           -e CERTIFCATE=1234-certificate.pem.crt \
           -e PRIVATE_KEY=1234-private.pem.key \
           -e THING_NAME=myFirstThing \
           -e IOT_ENDPOINT=abcdefg-ats.iot.eu-west-1.amazonaws.com \
           -i \
           -t iot-hands-on:1.0.0
```

# Application

Once started the container runs the following modified example [code](/Docker/aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py)

This example is modified to:

- Send the CPU usage to the Chat application in a room called "cpu"
- Respond to any questions asked send to a chat room with the name of this thing.