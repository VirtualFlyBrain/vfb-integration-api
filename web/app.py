# app.py - a minimal flask api using flask_restful
from flask import Flask, Response
from flask_restful import Resource, Api
import rdflib
import os
import urllib
import requests

app = Flask(__name__)
api = Api(app)

class TripleStore():
    endpoint = os.environ['SPARQLENDPOINT']

    def query(self,q):
        query=self.endpoint+q
        print(query)
        r = requests.get(query)
        return r.text

    def query_and_merge(self, q, dir):
        sparql_files = [x for x in os.listdir(os.path.join(app.root_path, 'sparql', dir)) if x.endswith('.sparql')]
        g = rdflib.Graph()
        for sparql_f in sparql_files:
            with app.open_resource("sparql/"+dir+"/"+sparql_f) as f:
                contents = f.read()
                if len(contents):
                    query_encoded = urllib.quote(str(contents))
                    try:
                        result = self.query(query_encoded)
                        try:
                            g.parse(data=result, format="ttl" )
                        except Exception as e:
                            print("Parsing failed.")
                            print(e)
                    except Exception as e:
                        print("VFB REST call failed: "+self.endpoint+query_encoded)
                        print(e)

        return g.serialize(format='xml')


ts = TripleStore()

class ProdInput(Resource):
    def get(self):
        return Response(ts.query_and_merge("q","prod"), mimetype='text/xml')

class OwleryInput(Resource):
    def get(self):
        return Response(ts.query_and_merge("q", "owlery"), mimetype='text/xml')

class TestInput(Resource):
    def get(self):
        return Response(ts.query_and_merge("q", "test"), mimetype='text/xml')

api.add_resource(OwleryInput, '/owlery')
api.add_resource(ProdInput, '/prod')
api.add_resource(TestInput, '/test')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')