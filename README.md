
# finfy-superend-docker

Superend (All in one backend) for finfy app and portal! Uses docker for easy deployment.
## Deployment
Clone this repository and follow the below mentioned steps to install with/without docker.

#### With docker
_easy asf, cd to project root and do:_
```bash
docker-compose up
```
Wait and your server will be up and running :P

#### Without docker
_A little tedious but do:_
```bash
pip install -r requirements.txt
```
_and finally_
```bash
python manage.py runserver 80
```
