#!/bin/bash

# Build docker image
docker build -t bank-flask:1.0 .

# Compose container
docker-compose up -d

echo "";
echo "Go http://localhost:5001/apidocs to see Bank-portal API docs interface";