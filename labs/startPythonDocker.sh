#!/bin/bash
echo "##########################################################"
echo " A docker image for python  development: "
echo
name="aws-python"
port=5000
if [[ $# != 0 ]]
then
    name=$1
    port=$2
fi

docker run --rm --name $name -v $(pwd):/usr/src/app -it  -v ~/.aws:/root/.aws -p $port:$port jbcodeforce/aws-python bash 
