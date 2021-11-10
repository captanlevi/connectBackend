FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
RUN useradd -m rushi
USER rushi
CMD ["bash","run.sh"]