FROM python:latest
COPY . /app
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 80
CMD python __main__.py