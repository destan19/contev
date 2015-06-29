#!/bin/sh
killall python
python manage.py  runserver 192.168.17.130:80 &
