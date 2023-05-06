FROM python:3.10.9-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY thebook/ /app
WORKDIR /app
CMD ["gunicorn", "thebook.wsgi:application", "--bind", "0:8000" ]