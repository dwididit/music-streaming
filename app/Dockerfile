FROM python:3.10

WORKDIR /app
COPY app/requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "app.py"]
