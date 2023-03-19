#!/bin/bash
# https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/ 
#  Not available in Windows
#  -k gevent -w 2 # 2>&1 >> ${LOGFILE} --access-logfile '-'
LOGFILE=./wsgi.log
touch ${LOGFILE} &&
(gunicorn --bind 0.0.0.0:5000 --error-logfile ${LOGFILE} --access-logfile ${LOGFILE} --capture-output 'flask_main:app' &
tail -f ${LOGFILE})