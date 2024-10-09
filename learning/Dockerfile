FROM python:3.12

RUN mkdir django_app
WORKDIR django_app

ADD requirements.txt /django_app/
RUN pip install -r requirements.txt

ADD . /django_app/
ADD .env.docker /django_app/.env

CMD python manage.py runserver 0.0.0.0:8000
