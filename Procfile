web: newrelic-admin run-program gunicorn --pythonpath="$PWD/drfunapp" wsgi:application
worker: python drfunapp/manage.py rqworker default