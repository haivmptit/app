FROM python:3.6
RUN apt update
RUN apt install libgl1-mesa-glx -y
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000