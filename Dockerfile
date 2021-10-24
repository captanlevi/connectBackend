FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install celery
RUN pip3 install redis
RUN pip3 install django-cors-headers
EXPOSE 8000
CMD ["bash","run.sh"]