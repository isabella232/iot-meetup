
docker load < output/iot-hands-on-1.0.0.docker.tar

docker run -v "<directory to certificate>":/tmp \
           -e CERTIFCATE=<certificate file name e.g. 1234-certificate.pem.crt> \
           -e PRIVATE_KEY=<private key file name e.g. 1234-private.pem.key> \
           -e THING_NAME=<your thing name> \
           -e IOT_ENDPOINT=a3g5girgh7pd7z-ats.iot.eu-west-1.amazonaws.com \
           -i \
           -t iot-hands-on:1.0.0
