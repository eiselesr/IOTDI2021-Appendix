#!/bin/bash

NAME=${PWD##*/}
docker build --tag "$NAME:1.0" -f Dockerfile .