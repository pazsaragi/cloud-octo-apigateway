#!/usr/bin/env bash
printf "Configuring localstack components..."

sleep 5

poetry run awslocal sqs create-queue --queue-name order-queue
poetry run awslocal dynamodb create-table --cli-input-json file://auth-table.json

printf "Done.\n"