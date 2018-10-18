from flask.views import MethodView
from flask import jsonify, request, abort, render_template, make_response
from flask_restful import Resource
import uuid
import json
import rdflib
from owlready2 import *
import types


# from app.decorators import app_required
from server.settings import ONTOLOGIES_DIRECTORY

class ConceptListController(Resource):
    def put(self, ontology):
        payload = request.json
        concept = payload.get('concept')
        parent = payload.get('parent')
        onto = get_ontology(
            "{}/{}.owl".format(ONTOLOGIES_DIRECTORY,ontology)
            ).load()
        concepts = list(onto.classes())
        concept_names = list(map(lambda concept: str(concept), concepts))
        parent_index = concept_names.index(parent)
        with onto:
            NewClass = types.new_class(concept, (concepts[parent_index],))
        response = {
            'status': 'Created new concept'
        }
        return response, 200

    def delete(self, ontology):
        payload = request.json
        concept = payload.get('concept')
        onto = get_ontology(
            "{}/{}.owl".format(ONTOLOGIES_DIRECTORY,ontology)
            ).load()
        concepts = list(onto.classes())
        concept_names = list(map(lambda concept: str(concept), concepts))
        concept_index = concept_names.index(concept)
        destroy_entity(concepts[concept_index])
        response = jsonify({})
        response.status_code = 204
        return response


class OntologyListController(Resource):
    def post(self):
        payload = request.json
        ontologies = payload.get('ontologies')
        g1 = rdflib.Graph()
        print(g1)
        g1.parse('{}/{}.owl'.format(ONTOLOGIES_DIRECTORY, ontologies[0]))

        g2 = rdflib.Graph()
        g2.parse('{}/{}.owl'.format(ONTOLOGIES_DIRECTORY, ontologies[1]))

        graph = g1 + g2
        output_path = '{}/{}_{}_fusion.owl'.format(
                ONTOLOGIES_DIRECTORY,
                ontologies[0],
                ontologies[1],)
        graph.serialize(
            destination=output_path, 
            format='xml')
        
        response = {'status': '{} and {} are merged in file {}'.format(
            ontologies[0], 
            ontologies[1],
            output_path,
            )}
        return response, 201

