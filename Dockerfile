# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3
ENV SPI_PATH /app/src/SPI-Py
WORKDIR /app

RUN apt-get update 
RUN apt-get install -y libzbar0 i2c-tools python3-smbus


RUN pip install --upgrade pip setuptools

COPY requirements.txt .

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
RUN pip3 install --no-cache-dir rpi.gpio\
 smbus

COPY ./src ./src

WORKDIR $SPI_PATH
RUN python3 setup.py install

WORKDIR /app/src

CMD ["python3", "main.py"]