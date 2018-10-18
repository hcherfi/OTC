from flask import Blueprint
from flask_restful import Api

# from server.application import output_xml
from .controllers import OntologyListController, ConceptListController

otc_blueprint = Blueprint('otc_app', __name__, template_folder='./views')
otc_api = Api(otc_blueprint)  # , default_mediatype='application/xml')
# otc_api.representations['application/xml'] = output_xml


otc_api.add_resource(OntologyListController, '/ontologies')
otc_api.add_resource(ConceptListController, '/concepts/<ontology>')


