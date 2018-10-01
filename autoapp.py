from backend_server.app import create_app

from sqlalchemy_utils import database_exists,create_database
from backend_server.extensions import db

app = create_app()

#for demonstration purposes only - this will build the database on the first run
with app.app_context():
    engine =  db.get_engine(bind='CRM')
    if database_exists(engine.url):
        print ' * Database Ready'
    else:
        print ' * Database Not Found...'
        print ' * Building Data Model...'
        new_db = create_database(engine.url)
        db.create_all(bind='CRM')
        print ' * Database Built'
