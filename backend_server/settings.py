# -*- coding: utf-8 -*-
import os
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_BINDS = {
    'CRM':        'mysql+pymysql://root:password@localhost/crm'
    #extract database bindings go here
##    'appmeta':      'sqlite:////path/to/appmeta.db'
}
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False