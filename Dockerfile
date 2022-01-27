FROM python:3.9.7

WORKDIR .
COPY . .
RUN pip install --upgrade pip install -r requirements.txt
RUN ls
EXPOSE 8000:9100

CMD ["python", "main.py"]