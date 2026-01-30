#!/bin/bash

pip install -e .

docker pull mongo
docker-compose up -d

