#!/bin/bash
echo "##########################################################"
echo " A docker image for python  development: "
echo "For cdk... once started do in /app:"
echo "  python3 -m venv .venv"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
name="aws-python"
port=5000
if [[ $# != 0 ]]
then
    name=$1
    port=$2
fi

docker run --rm --name $name -v $(pwd):/app -it  -v ~/.aws:/root/.aws -p $port:$port jbcodeforce/aws-python bash 
