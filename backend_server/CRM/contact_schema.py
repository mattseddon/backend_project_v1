from backend_server.extensions import ma
from backend_server.data_handler import ModelSchema, Schema

from contact_model import ContactModel,ContactCompanyLinkModel

class ContactModelSchema(ModelSchema):
    class Meta:
         model = ContactModel

class ContactCompanyLinkModelSchema(ModelSchema):
    class Meta:
         model = ContactCompanyLinkModel

class ContactCompaniesSchema(Schema):
    class Meta:
        fields = ('phone','email','title','website','id','created','updated')
        model = ContactModel

class ContactUpdateSchema(Schema):
    class Meta:
        fields = ('first_name','surname','phone','email')

#base for interface to API
class ContactSchema(Schema):
    class Meta:
        fields = ('id','first_name','surname','companies')
        contacts = ma.Nested(ContactCompaniesSchema)