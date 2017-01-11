#!/bin/bash

# Deploy the project on PCF

if [ "$#" -ne 3 ]
then
  echo "Usage: deploy.sh S3_BUCKET_NAME AWS_ACCESS_KEY AWS_SECRET_KEY"
  exit 1
fi


S3_BUCKET_NAME=${1}
AWS_ACCESS_KEY=${2}
AWS_SECRET_KEY=${3}

cp manifest.yml manifest.yml.bck
sed -i -e "s#S3_BUCKET_NAME: bucket#S3_BUCKET_NAME: ${S3_BUCKET_NAME}#" manifest.yml
sed -i -e "s#AWS_ACCESS_KEY: key#AWS_ACCESS_KEY: ${AWS_ACCESS_KEY}#" manifest.yml
sed -i -e "s#AWS_SECRET_KEY: secret#AWS_SECRET_KEY: ${AWS_SECRET_KEY}#" manifest.yml

cf push

mv manifest.yml.bck manifest.yml
