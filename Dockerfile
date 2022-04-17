FROM centos:7.9.2009

RUN yum update -y && yum install -y python3
RUN pip3 install pytest==7.0.0
RUN pip3 install --user xmltodict
RUN mkdir /code
RUN pip3 install flask

COPY app.py /code/app.py
COPY pytest_app.py /code/pytest_app.py
COPY cities.xml /code/cities.xml
COPY positions.xml /code/positions.xml
COPY . /app

RUN chmod +rx /code/app.py
RUN chmod +rx /code/pytest_app.py

ENV PATH "/code:$PATH"
