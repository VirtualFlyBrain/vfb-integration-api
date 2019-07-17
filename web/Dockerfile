FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ENV SPARQLENDPOINT="http://ts.nico.virtualflybrain.org/rdf4j-server/repositories/test?query="
ENV FLASK_APP=app.py
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run", "--host=0.0.0.0"]