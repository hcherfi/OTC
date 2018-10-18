from flask import Flask  # , make_response
from subprocess import call
# from simplexml import dumps
import os
import sys

# def output_xml(data, code, headers=None):
#    """Makes a Flask response with a XML encoded body"""
#    resp = make_response(dumps({'response' :data}), code)
#    resp.headers.extend(headers or {})
#    resp.headers['content-type'] = 'application/xml'
#    return resp


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def create_app(**config_overrides):
    app = Flask(__name__, static_url_path='')  # , template_folder="../public", static_folder="../public")

    # app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)

    # import blueprints
    # from store.views import store_app
    from otc import otc_blueprint
    # from app.views import app_app

    # register blueprints
    app.register_blueprint(otc_blueprint)
    # app.register_blueprint(app_app)

    return app
