FROM python:3.9.10-bullseye

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /
CMD [ "python3", "system-sensors.py"]
