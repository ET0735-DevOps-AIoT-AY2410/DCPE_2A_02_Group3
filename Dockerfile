# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3
ENV SPI_PATH /app/src/SPI-Py
WORKDIR /app

RUN apt-get update && \
    apt-get install -y cmake ninja-build build-essential libcap-dev \
    libcamera0.0.3 libcamera-v4l2 libcamera-ipa

RUN pip install --upgrade pip setuptools

COPY requirements.txt .

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
RUN pip3 install --no-cache-dir rpi.gpio\ smbus

COPY src /app/src

WORKDIR $SPI_PATH
RUN python3 setup.py install

WORKDIR /app

CMD ["python3", "src/main.py"]