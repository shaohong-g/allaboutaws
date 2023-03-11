# https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/ 
#  Not available in Windows
#  -k gevent -w 2
LOGFILE=./wsgi.log
gunicorn --bind 127.0.0.1:5000 --access-logfile '-' 'flask_main:app' 2>&1 >> ${LOGFILE}