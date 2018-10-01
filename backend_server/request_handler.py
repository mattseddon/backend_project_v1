from flask import jsonify,request,Response
from datetime import datetime

class HandleRequestWith():
    def __init__(self,InterfaceObject):
        self.Interface = InterfaceObject.Interface

    def get_one(self,id):
        return self.Interface.model_schema_to_dump_one.get_one_as_json(id)
        #)

    def get_all(self):
        return jsonify(
            self.Interface.model_schema_to_dump_all.get_all_as_json()
            )

    def get_children(self,id):
        return jsonify(
            self.Interface.schema_to_dump_children.get_children_as_json(id)
            )

    def post_one_to_many(self,request):
        parent_loader = self.Interface.model_schema_to_load_data
        child_loader = self.Interface.model_schema_to_load_child_data
        child_link_loader = self.Interface.model_schema_to_load_child_link_data

        request_data = request.get_json()
        request_loaded_in_one_to_many_schema = self.Interface.schema_to_load_post_request.make_object_from(request_data)

        first_missing_column = parent_loader.validate_data_against_schema(request_loaded_in_one_to_many_schema)
        if first_missing_column:
            api_response = self.generate_error_as_record("must contain",first_missing_column)
            api_response.update(request_loaded_in_one_to_many_schema)

        else:
            api_response = {}

            #create an ID which will be used to generate the link record if all goes well
            provisional_parent_id = parent_loader.create_id_if_not_provided_in(
                                        parent_loader.make_object_from(request_loaded_in_one_to_many_schema)
                                        )

            children = request_loaded_in_one_to_many_schema.get(self.Interface.name_of_child_object)
            has_valid_children = False
            if children:
                api_response_to_children = []
                for child in children:
                    #validate both child and link before loading anything
                    first_missing_child_column = child_loader.validate_data_against_schema(child)
                    first_missing_link_column = child_link_loader.validate_data_against_schema(child)
                    if first_missing_child_column or first_missing_link_column:
                        api_response_to_child = self.generate_error_as_record(
                                                    "must contain",(first_missing_child_column or first_missing_link_column)
                                                    )
                        api_response_to_child.update(child)
                    else:
                        has_valid_children = True
                        api_response_to_child = self.generate_response_from(
                                                    child_loader.try_load(child)
                                                    )
                        api_response_to_child.update(child)#this seems like a duplicate but will load the 'link' information into the message

                        child[self.Interface.name_of_id_for_link] = str(provisional_parent_id)
                        child[self.Interface.name_of_child_id_for_link] = api_response_to_child.get('id')
                        child_link_loader.try_load(child)

                    api_response_to_children.append(api_response_to_child)
                api_response.update({self.Interface.name_of_child_object:api_response_to_children})
            else:
                api_response.update({self.Interface.name_of_child_object:"none entered"})

            if (      (self.Interface.requires_valid_children and has_valid_children)
                or not(self.Interface.requires_valid_children)):
                api_response_to_parent = self.generate_response_from(
                                            parent_loader.try_load(request_loaded_in_one_to_many_schema)
                                            )

            else:
                api_response_to_parent = {"status" : "nothing loaded, parent record requires at least one valid child"}

            api_response.update(api_response_to_parent)

        return jsonify(
            api_response
            )

    #update
    def put_one(self,request,id,link_id):
        request_data = request.get_json()

        if self.Interface.requires_valid_children and link_id is None:
            return jsonify({"message": "The method is not allowed for the requested URL."})

        else:
            parent_updator = self.Interface.model_schema_to_load_data
            first_primary_key = parent_updator.validate_data_contains_no_primary_keys(request_data)
            #validate everything before making any changes
            if first_primary_key:
                return jsonify(
                    self.generate_error_as_record("must not contain",first_primary_key)
                    )
            if link_id:
                link_id = id+'|'+link_id
                link_updator = self.Interface.model_schema_to_load_child_link_data
                first_primary_key = link_updator.validate_data_contains_no_primary_keys(request_data)
                if first_primary_key:
                    return jsonify(
                        self.generate_error_as_record("must not contain",first_primary_key)
                        )

            api_reponse = self.generate_response_from(
                            parent_updator.try_update(id,request_data)
                            )

            if link_id:
                #this line means that all IDs in all link tables must be setup as child then parent
                #and data can only be updated for the child at the child level not from "top down"
                link_response =link_updator.try_update(link_id,request_data)
                if link_response.updated:
                    api_reponse.update(self.generate_response_from(link_response))
                    del api_reponse['id']

        return jsonify(
                    api_reponse
                    )

    @staticmethod
    def generate_response_from(loader_reponse):
        item_name = loader_reponse.data_loaded_in_model.__tablename__
        if loader_reponse.existing:
            if loader_reponse.updated:
                response = {"status": "%s updated" % item_name}
            else:
                response = {"status": "%s is existing and unchanged" % item_name}
        else:
            response = {"status":"%s created" % item_name}

        response.update(loader_reponse.data_as_json)
        return response

    @staticmethod
    def generate_error_as_record(reason,error):
        return {'error' : "!!! ERROR - record %s %s, record rejected !!!" % (reason,error)}