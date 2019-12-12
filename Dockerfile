FROM python:3.7-latest
COPY . /app
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD python __main__.py