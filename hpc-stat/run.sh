#!/bin/bash

docker run -p 9050:80 -p 7001:17001 -p 7002:17002 \
	-v `pwd`/uwsgi.ini:/hpc-stat/uwsgi.ini \
	-v `pwd`/local.py:/hpc-stat/local.py \
	-v `pwd`/nginx.conf:/etc/nginx/nginx.conf \
	-v `pwd`/log:/log \
	-v `pwd`/start.sh:/start.sh \
	--name clustername-data-api \
	-d hpc01/data-stat:`date +%y%m%d`
