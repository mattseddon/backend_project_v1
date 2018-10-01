# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from backend_server.extensions import db,ma
from CRM.contact_resource import crm_contact_api_bp
from CRM.company_resource import crm_company_api_bp


def create_app(config_object='backend_server.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    ma.init_app(ma)
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(crm_contact_api_bp)
    app.register_blueprint(crm_company_api_bp)
    return None