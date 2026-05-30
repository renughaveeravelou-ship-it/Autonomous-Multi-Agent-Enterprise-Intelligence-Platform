#!/bin/bash

docker-compose build

docker-compose up -d

kubectl apply -f deployment/kubernetes/