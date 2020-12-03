This project is about to to get current total no of covid active cases in a country

Project architecture
 
 ![](image1.png?raw=true)

Deployed on AWS EC2 Instance


Prerequisite  
Clone repo and create a virtual env  
install packages from requirements.txt  
Change the user and password of db accordingly in settings.py  

To make db migrations, run these commands
python manage.py migrate

django_rq  - a Redis based Python queuing library
https://github.com/rq/django-rq

api to get total active cases in india
http://3.138.197.21/polls/cases/in/

