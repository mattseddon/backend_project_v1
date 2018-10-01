from flask import jsonify
from backend_server.extensions import ma
import re

class MarshalMixin():

    def get_one_as_json(self,id):
        return self.make_json_from(
            self.get_one_as_model(id)
            )

    def get_one_as_model(self,id):
        return self.Meta.model.get_one_from_db(id)

    def get_all_as_json(self):
        return self.make_json_from(
                    self.Meta.model.get_all_from_db()
                )

    def get_children_as_json(self,id):
        return self.make_json_from(
                self.Meta.model.get_children_from_db(id)
                )

    def make_json_from(self,dbquery):
        return self.dump(dbquery).data

    def make_object_from(self,data):
        return self.load(data).data

    def get_columns_with_no_data(self,data,required_columns):
        invalid_columns = []
        for column in required_columns:
            if data.get(column) is None:
                invalid_columns.append(column)
        return invalid_columns

    def create_id_from(self,data_loaded_in_model,columns,separator):
        data = data_loaded_in_model.coerce_columns_to_dict(columns)
        cleaned_data = remove_special_characters_from(columns,data)
        for i,column in enumerate(columns):
            if i==0:
                new_id  = cleaned_data[column]
            else:
                new_id = new_id + ' ' + cleaned_data[column]
        new_id = new_id.lower().replace(' ',separator)
        return new_id

    def validate_data_against_schema(self,data):
        invalid_data = self.get_invalid_data(data)
        if invalid_data:
            first_invalid_column = invalid_data[0]
            return first_invalid_column

    def try_load(self,data):
        self.data_loaded_in_model = self.make_object_from(data)
        self.data_loaded_in_model.id = self.create_id_if_not_provided_in(self.data_loaded_in_model)
        Existing = self.data_loaded_in_model.search_db_for_id()
        if Existing:
            self.data_loaded_in_model = Existing
            self.existing = True
            self.updated = False
        else:
            self.data_loaded_in_model.save_in_db()
            self.existing = False
        self.data_as_json = self.make_json_from(self.data_loaded_in_model)
        return self

    def create_id_if_not_provided_in(self,data_loaded_in_model):
        if data_loaded_in_model.id is None:
            new_id = self.create_id_from(data_loaded_in_model,
                                         data_loaded_in_model.primary_key_created_from,
                                         data_loaded_in_model.primary_key_separator)
        else:
            new_id = data_loaded_in_model.id
        return new_id

    def try_update(self,id,data):
        self.data_loaded_in_model = self.get_one_as_model(id)
        if self.data_loaded_in_model:
            self.existing = True
            changes_needed = self.data_loaded_in_model.check_data_for_changes(data)
            if changes_needed:
                self.data_loaded_in_model.update_db_with(data)
                self.updated = True
            else:
                self.updated = False
            self.data_as_json = self.make_json_from(self.data_loaded_in_model)
        return self

    @classmethod
    def validate_data_contains_no_primary_keys(self,data):
        primary_keys = self.Meta.model.get_primary_keys()
        for key,value in data.items():
            if key in primary_keys: return key

class ModelSchema(ma.ModelSchema,MarshalMixin):

    def get_invalid_data(self,data):
        required_columns=self.Meta.model.get_required_columns()
        columns_with_no_data = self.get_columns_with_no_data(data,required_columns)
        return columns_with_no_data

class Schema(ma.Schema,MarshalMixin):

    def get_invalid_data(self,data):
        required_columns = [column for column in self.Meta.fields if column not in ['created','updated','id']]
        columns_with_no_data = self.get_columns_with_no_data(data,required_columns)
        return columns_with_no_data

def remove_special_characters_from(columns_to_clean,data):

    for column in columns_to_clean:
        data[column] = re.sub('[^A-z0-9\s\.]', ' ', data[column])
        data[column] = re.sub('\s+'          , ' ', data[column])
        data[column] = re.sub('(^\s|\s$)'    , '' , data[column])

    return data
