cd /pipeline/vfb-integration-api/web
docker build -t matentzn/vfb-integration-api . 
docker run -p 5000:5000 -e SPARQLENDPOINT=http://ts.p2.virtualflybrain.org/rdf4j-server/repositories/vfb?query= matentzn/vfb-integration-api