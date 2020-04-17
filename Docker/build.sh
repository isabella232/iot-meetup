#!/bin/sh
export DOCKER_VERSION="1.0.0"

# Build the docker image
docker build . --tag=iot-hands-on:${DOCKER_VERSION}

# Export the docker image
if [ ! -e output ]; then
    mkdir output
fi 
docker save -o output/iot-hands-on-${DOCKER_VERSION}.docker.tar iot-hands-on:${DOCKER_VERSION}

export TEST_RUN_FILE_UNIX=run.sh
export TEST_RUN_FILE_WINDOWS=run.cmd

# Delete the old files
rm -f ${TEST_RUN_FILE_UNIX}
rm -f ${TEST_RUN_FILE_WINDOWS}

# Create a test run file to run with the current version
echo "#!/bin/sh"                                                                                  >> ${TEST_RUN_FILE_UNIX}
echo ""                                                                                           >> ${TEST_RUN_FILE_UNIX}
echo "docker load < output/iot-hands-on-${DOCKER_VERSION}.docker.tar"                             >> ${TEST_RUN_FILE_UNIX}
echo ""                                                                                           >> ${TEST_RUN_FILE_UNIX}
echo 'docker run -v "<directory to certificate>":/tmp \\'                                         >> ${TEST_RUN_FILE_UNIX}
echo "           -e CERTIFCATE=<certificate file name e.g. 1234-certificate.pem.crt> \\"          >> ${TEST_RUN_FILE_UNIX}
echo "           -e PRIVATE_KEY=<private key file name e.g. 1234-private.pem.key> \\"             >> ${TEST_RUN_FILE_UNIX}
echo "           -e THING_NAME=<your thing name> \\"                                              >> ${TEST_RUN_FILE_UNIX}
echo "           -e IOT_ENDPOINT=a3g5girgh7pd7z-ats.iot.eu-west-1.amazonaws.com \\"               >> ${TEST_RUN_FILE_UNIX}
echo "           -i \\"                                                                           >> ${TEST_RUN_FILE_UNIX}
echo "           -t iot-hands-on:${DOCKER_VERSION}"                                               >> ${TEST_RUN_FILE_UNIX}
chmod 755 run.sh

echo ""                                                                                           >> ${TEST_RUN_FILE_WINDOWS}
echo "docker load < output/iot-hands-on-${DOCKER_VERSION}.docker.tar"                             >> ${TEST_RUN_FILE_WINDOWS}
echo ""                                                                                           >> ${TEST_RUN_FILE_WINDOWS}
echo 'docker run -v "<directory to certificate>":/tmp \\'                                         >> ${TEST_RUN_FILE_WINDOWS}
echo "           -e CERTIFCATE=<certificate file name e.g. 1234-certificate.pem.crt> \\"          >> ${TEST_RUN_FILE_WINDOWS}
echo "           -e PRIVATE_KEY=<private key file name e.g. 1234-private.pem.key> \\"             >> ${TEST_RUN_FILE_WINDOWS}
echo "           -e THING_NAME=<your thing name> \\"                                              >> ${TEST_RUN_FILE_WINDOWS}
echo "           -e IOT_ENDPOINT=a3g5girgh7pd7z-ats.iot.eu-west-1.amazonaws.com \\"               >> ${TEST_RUN_FILE_WINDOWS}
echo "           -i \\"                                                                           >> ${TEST_RUN_FILE_WINDOWS}
echo "           -t iot-hands-on:${DOCKER_VERSION}"                                               >> ${TEST_RUN_FILE_WINDOWS}
