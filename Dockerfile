FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY pip.conf /code/
RUN mkdir ~/.pip/ && cp pip.conf ~/.pip/
RUN pip install -r requirements.txt
