# project1

Start app:
```
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
## OR
```
gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemonize
```
Kill app:
```
pkill gunicorn
```
---
# package requirements:
```
sudo apt-get install libpq-dev
```
