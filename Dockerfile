FROM python:3.8-slim

RUN python -m pip install --upgrade pip

WORKDIR /XML-RPC_API_SERVER

COPY . .

RUN python -m pip install -r requirements.txt

RUN python main.py
