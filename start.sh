#!/bin/sh
sudo docker kill tutor

sudo docker-compose build
sudo docker-compose up
