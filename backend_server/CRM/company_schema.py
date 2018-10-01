from backend_server.extensions import ma
from backend_server.data_handler import ModelSchema, Schema

from company_model import CompanyModel

#marshmallow object relational mapper converter - serialise / de-serialise ORMs
class CompanyModelSchema(ModelSchema):
    class Meta:
        model = CompanyModel

#marshmallow object marshaller - serialise / de-serialise objects - not built from SQL Alchemy ORM object
class CompanyContactsSchema(Schema):
    class Meta:
        fields = ('phone','email','first_name','surname','id','created','updated')
        #FYI only - the model attribute is provided here only so that get_children can be called from the schema (by request_handler)
        model = CompanyModel

#base for POST requests
class CompanySchema(Schema):
    class Meta:
        fields = ('id','title','website','contacts')
        contacts = ma.Nested(CompanyContactsSchema)