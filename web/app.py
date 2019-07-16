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
        r = requests.get(self.endpoint+q)
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
                        g.parse(data=self.query(query_encoded))
                    except:
                        print("VFB REST call failed: "+self.endpoint)
                        print("Query: "+query_encoded)

        return g.serialize(format='xml')


ts = TripleStore()

class ProdInput(Resource):
    def get(self):
        return Response(ts.query_and_merge("q","prod"), mimetype='text/xml')

class OwleryInput(Resource):
    def get(self):
        return Response(ts.query_and_merge("q", "owlery"), mimetype='text/xml')

api.add_resource(OwleryInput, '/owlery')
api.add_resource(ProdInput, '/prod')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')