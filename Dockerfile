FROM python:3.9.10-bullseye

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /src
CMD [ "python3", "-u", "system-sensors.py"]
