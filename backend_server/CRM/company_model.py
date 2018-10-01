from backend_server.sql_database import Column, Model
from backend_server.extensions import db
from model import CRMMixin
import contact_model

class CompanyModel(Model,CRMMixin):
    __tablename__ = 'company'
    primary_key_created_from = ['title']
    primary_key_separator = '.'

    def pkdefault(context):
        return self.auto_generate_default_primary_key(context)

    id = Column(db.String(100), primary_key=True,default=pkdefault,nullable=False)
    title = Column(db.String(100),nullable=False)
    website = Column(db.String(100),nullable=False)

    @staticmethod
    def get_children_from_db(id):
        return  db.session.query(contact_model.ContactCompanyLinkModel.created,
                                 contact_model.ContactCompanyLinkModel.updated,
                                 contact_model.ContactCompanyLinkModel.email,
                                 contact_model.ContactCompanyLinkModel.phone,
                                 contact_model.ContactModel.id,
                                 contact_model.ContactModel.first_name,
                                 contact_model.ContactModel.surname)\
                          .join(contact_model.ContactModel,
                                contact_model.ContactCompanyLinkModel.contact_id == contact_model.ContactModel.id)\
                          .filter(contact_model.ContactCompanyLinkModel.company_id==id)