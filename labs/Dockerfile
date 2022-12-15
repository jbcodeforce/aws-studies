FROM node:14-alpine

# Install packages
RUN apk update && apk add --update --no-cache \
    git \
    bash \
    curl \
    openssh \
    python3 \
    py3-pip \
    py-cryptography \
    wget \
    curl

RUN apk --no-cache add --virtual builds-deps build-base 

# Update NPM
RUN npm config set unsafe-perm true
RUN npm update

# Install AWSCLI
RUN pip install --upgrade pip && \
    pip install --upgrade awscli aws-cdk-lib pipenv boto3  psycopg2-binary

# Install Serverless Framework
RUN npm install -g serverless aws-cdk

WORKDIR /app