from backend_server.extensions import Api, Blueprint, Resource
from backend_server.request_handler import HandleRequestWith, request

from company_schema import CompanySchema,CompanyModelSchema,CompanyContactsSchema
from contact_schema import ContactModelSchema,ContactCompanyLinkModelSchema

crm_company_api_bp = Blueprint('crm_customer_api', __name__)
api = Api(crm_company_api_bp)

class Company():
    class Interface():
        schema_to_load_post_request = CompanySchema()

        name_of_child_object = 'contacts'
        name_of_child_id_for_link = 'contact_id'
        name_of_id_for_link = 'company_id'
        requires_valid_children = False

        model_schema_to_load_data = CompanyModelSchema()
        model_schema_to_load_child_data = ContactModelSchema()
        model_schema_to_load_child_link_data = ContactCompanyLinkModelSchema()

        model_schema_to_dump_one = CompanyModelSchema()
        model_schema_to_dump_all = CompanyModelSchema(many=True)
        schema_to_dump_children  = CompanyContactsSchema(many=True)

company_interface = Company()
api_company_request_handler = HandleRequestWith(company_interface)

class GetCompany(Resource):
    def get(self, id):
        return api_company_request_handler.get_one(id)

class GetCompanies(Resource):
    def get(self):
        return api_company_request_handler.get_all()

class GetCompanyContacts(Resource):
    def get(self, id):
        return api_company_request_handler.get_children(id)

class PostCompany(Resource):
    def post(self):
        return  api_company_request_handler.post_one_to_many(request)

class PutCompany(Resource):
    def put(self,id):
        return  api_company_request_handler.put_one(request,id,None)

api.add_resource(GetCompany, '/company/<string:id>')
api.add_resource(GetCompanies, '/companies')
api.add_resource(GetCompanyContacts, '/company/<string:id>/contacts')

api.add_resource(PostCompany, '/company')
api.add_resource(PutCompany, '/company/<string:id>')



