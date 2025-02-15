#!/bin/bash

mkdir -p uploads output/images output/scripts output/audio static

if command -v docker-compose &> /dev/null; then
    echo "Using docker-compose..."
    docker-compose up --build
else
    echo "Using docker compose..."
    docker compose up --build
fi