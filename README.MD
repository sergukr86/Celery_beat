1. Install dependencies:

'''
pip install -r requirements.txt
'''

2. Run docker process:

'''
docker run -d -p 5672:5672 rabbitmq
'''

3. Run django-celery-beat:

'''
celery -A celery_beat beat
'''

4. Run worker process

'''
celery -A celery_beat worker -l INFO 
'''

5. Run Django webserver 

'''
python manage.py runserver
'''