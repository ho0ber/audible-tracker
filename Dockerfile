FROM python:3.11-alpine

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app .

EXPOSE 9999
CMD [ "python3", "tracker.py"]
