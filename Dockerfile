FROM balenalib/raspberry-pi-debian-python:3.11

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app .

EXPOSE 9999
CMD [ "python3", "tracker.py"]
