from backend_server.extensions import Api, Blueprint, Resource
from backend_server.request_handler import HandleRequestWith, request

from contact_schema import ContactModelSchema,ContactSchema,ContactCompanyLinkModelSchema,ContactCompaniesSchema,ContactUpdateSchema
from company_schema import CompanyModelSchema

crm_contact_api_bp = Blueprint('crm_contact_api', __name__)
api = Api(crm_contact_api_bp)

#interface to API
class Contact():
    class Interface:
        schema_to_load_post_request = ContactSchema()

        name_of_child_object = 'companies'
        name_of_child_id_for_link = 'company_id'
        name_of_id_for_link = 'contact_id'
        requires_valid_children = True

        model_schema_to_load_data = ContactModelSchema()
        model_schema_to_load_child_data = CompanyModelSchema()
        model_schema_to_load_child_link_data = ContactCompanyLinkModelSchema()

        model_schema_to_dump_one = ContactModelSchema()
        model_schema_to_dump_all = ContactModelSchema(many=True)
        schema_to_dump_children  = ContactCompaniesSchema(many=True)

contact_interface = Contact()
api_contact_request_handler = HandleRequestWith(contact_interface)

class GetContact(Resource):
    def get(self, id):
        return api_contact_request_handler.get_one(id)

class GetContacts(Resource):
    def get(self):
        return api_contact_request_handler.get_all()

class GetContactCompanies(Resource):
    def get(self, id):
        return api_contact_request_handler.get_children(id)

class PostContact(Resource):
    def post(self):
        return  api_contact_request_handler.post_one_to_many(request)

class PutContact(Resource):
    def put(self,id,link_id):
        return api_contact_request_handler.put_one(request,id,link_id)

api.add_resource(GetContact, '/contact/<string:id>')
api.add_resource(GetContacts, '/contacts')
api.add_resource(GetContactCompanies, '/contact/<string:id>/companies')

api.add_resource(PostContact, '/contact')
api.add_resource(PutContact, '/contact/<string:id>/<string:link_id>')

