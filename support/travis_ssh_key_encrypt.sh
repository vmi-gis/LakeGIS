#!/bin/bash

SSH_KEY_PATH=$1

base64 --wrap=64 ${SSH_KEY_PATH} > ${SSH_KEY_PATH}_base64
for l in $(cat ${SSH_KEY_PATH}_base64);
do
	LINE=$(grep -n $l ${SSH_KEY_PATH}_base64 | cut -d: -f1)
	echo "- secure: $(travis encrypt \"SSH_KEY_$LINE=$l\")"
done

