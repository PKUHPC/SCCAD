#!/bin/sh
uwsgi --ini /hpc-stat/uwsgi.ini
nginx -g "daemon off;"
