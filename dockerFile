FROM ubuntu

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python3-pip
RUN pip3 install flask 
RUN pip3 install requests
RUN pip3 install pymssql


COPY app.py /opt/app.py

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0
