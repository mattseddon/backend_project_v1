from backend_server.sql_database import Column, Model
from backend_server.extensions import db
from model import CRMMixin
import company_model

class ContactModel(Model,CRMMixin):
    __tablename__ = 'contact'
    primary_key_created_from = ['first_name','surname']
    primary_key_separator = '.'

    def pkdefault(context):
        return self.auto_generate_default_primary_key(context)

    id = Column(db.String(100), primary_key=True,default=pkdefault,nullable=False)
    first_name = Column(db.String(100),nullable=False)
    surname = Column(db.String(100),nullable=False)

    @staticmethod
    def get_children_from_db(id):
        companiesQuery = db.session.query(ContactCompanyLinkModel.created,
                                          ContactCompanyLinkModel.updated,
                                          ContactCompanyLinkModel.email,
                                          ContactCompanyLinkModel.phone,
                                          company_model.CompanyModel.id,
                                          company_model.CompanyModel.title,
                                          company_model.CompanyModel.website)\
                                   .join(company_model.CompanyModel,
                                         ContactCompanyLinkModel.company_id == company_model.CompanyModel.id)\
                                   .filter(ContactCompanyLinkModel.contact_id==id)
        return companiesQuery

class ContactCompanyLinkModel(Model,CRMMixin):
    __tablename__ = 'contact_company_link'
    primary_key_created_from = ['contact_id','company_id']
    primary_key_separator = '|'

    #this is mitigated by the API but if no default is entered the primary keys then incoming data will not be marshalled into an object
    def pkdefault(context):
        return self.auto_generate_default_primary_key(context)

    id = db.Column(db.String(200), primary_key=True,default=pkdefault,nullable=True)#really did not want to include this field but no data would serealise automatically without it
    contact_id = Column(db.String(100),primary_key=True,nullable=False)
    company_id = Column(db.String(100),primary_key=True,nullable=False)
    email = Column(db.String(100),nullable=False)
    phone = Column(db.String(20),nullable=False)