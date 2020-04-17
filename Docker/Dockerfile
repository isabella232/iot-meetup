# Start from a basic alpine image with python
FROM python:3.6.1-alpine

# Add pip and the boto3 libraries
RUN apk update && \
    apk add openssl gcc linux-headers g++ python3-dev && \
    python3 -m ensurepip && \
    pip install --upgrade pip && \
    pip install boto3 pyspectator

# Copy in our local files
RUN mkdir /usr/src/work/
COPY aws-iot-device-sdk-python/ /usr/src/work/
COPY application/ /usr/src/work/
RUN cd /usr/src/work/ && \
    python setup.py install

# Make sure the application is started
CMD ["/bin/sh", "/usr/src/work/run.sh"]