FROM python:3.11

# Set environment variables
ENV BROKER=broker.emqx.io
ENV PORT=1883
ENV CLIENT_ID=BMS-Client
ENV TOPIC=Rubicon/BMS/Default/Raw
ENV QOS=0
ENV CLEAN_SESSION=True
ENV KEEP_ALIVE=60
ENV RECONNECT_ON_FAILURE=True
ENV USERNAME=None
ENV PASSWORD=None

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install paho-mqtt
RUN pip install python-dotenv


CMD [ "python", "./main.py" ]