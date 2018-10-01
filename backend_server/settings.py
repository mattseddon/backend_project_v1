import os
"""Application configuration.
"""
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_BINDS = {
    'CRM':        'mysql+pymysql://root:password@localhost/crm'

}
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False