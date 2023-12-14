FROM arm64v8/python:3.11-slim-bullseye as build

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]

