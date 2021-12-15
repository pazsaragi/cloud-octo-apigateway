#!/bin/bash
# 
# Builds a Docker image and pushes to an AWS ECR repository

set -e

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker build -t $REPO_NAME .

docker tag $REPO_NAME:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest

docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest