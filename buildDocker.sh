#!/bin/bash

echo "Install docker"

docker build -t app:vezdekod .
docker run -it -p 5000:5000 app:vezdekod

echo "Done"