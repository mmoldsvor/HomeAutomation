FROM alpine3.7
COPY . /app
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python __main__.py