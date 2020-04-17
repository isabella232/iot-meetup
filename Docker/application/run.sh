#!/bin/bash
echo "Starting Merapar Basic AWS IoT example"

# Point to the root certificate
ROOT_CA="usr/src/work/AmazonRootCA1.pem"
# not sure if it matters, but topics generally only accept lower case
THING_NAME_LOWER=$(echo ${THING_NAME} | tr '[:upper:]' '[:lower:]')

echo "Using startup command"
echo "python /usr/src/work/samples/basicPubSub/basicPubSub.py -r \"${ROOT_CA}\" -e \"${IOT_ENDPOINT}\" -c \"/tmp/${CERTIFCATE}\" -k \"/tmp/${PRIVATE_KEY}\" -id \"${THING_NAME}\" --mode both -t room/public/cpu/${THING_NAME} -s room/public/${THING_NAME_LOWER}"
echo ""
echo "Starting.."
python /usr/src/work/samples/basicPubSub/basicPubSub.py -r "${ROOT_CA}" -e "${IOT_ENDPOINT}" -c "/tmp/${CERTIFCATE}" -k "/tmp/${PRIVATE_KEY}" -id "${THING_NAME}" --mode both -t room/public/cpu/${THING_NAME} -s room/public/${THING_NAME_LOWER}
