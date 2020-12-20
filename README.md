# BankPortalAngular

## Prerequisites

Install following dependencies beforehand.

1. Docker, docker-compose:
[Docker home page](https://docs.docker.com/get-docker/)
2. Git

## Build and start docker containers

Run this command to build base image and start container

```bash
./build-and-start.sh
```

Run this command to build image, you need to re-build this image if requirements.txt change

```bash
docker build -t bank-flask:1.0 .
```

Run this command to start project without rebuild bank-flask image

```bash
docker-compose up -d
```

## Stop docker-compose containers

Run this command to stop project

```bash
docker-compose stop
```

## Remove docker-compose containers

Run this command to stops containers and removes containers, networks, volumes, and images created by up

```bash
docker-compose down
```

After container was started, go http://localhost:5001/apidocs to see Bank-portal API docs interface
