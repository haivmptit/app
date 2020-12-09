FROM python:3.6
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y --no-install-recommends apt-utils
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000