from extensions import db
from datetime import datetime

Column = db.Column
DateTime = db.DateTime

class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}
    """Mixin that adds methods for CRUD (create, read, update, delete) operations."""

    #create
    def save_in_db(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    #read
    @classmethod
    def get_one_from_db(self,id):
        return self.query.filter(self.id==id).first()

    #read
    @classmethod
    def get_all_from_db(self):
        return self.query.all()

    def update_db_with(self, changes, commit=True):
        for key, value in changes.items():
            setattr(self, key, value)
        return commit and self.save_in_db() or self

    def delete_from_db(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

class TimestampMixin(object):
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)


class Model(db.Model,CRUDMixin, TimestampMixin):
    __abstract__ = True

    def coerce_columns_to_dict(self,columns):
        return {column: getattr(self, column) for column in columns}

    def check_data_for_changes(self, changes):
        for key, new_value in changes.items():
            if key in self.get_required_columns():
                existing_value = getattr(self, key)
                if existing_value and existing_value != new_value:
                    return True
        else:
            return False

    @classmethod
    def get_primary_keys(self):
        return [column.name for column in self.__table__.primary_key]

    @classmethod
    def get_required_columns(self):
        primary_keys = self.get_primary_keys()
        exclude_list = ['created','updated']
        exclude_list.extend(primary_keys)
        return [column.name for column in self.__table__.columns if column.name not in exclude_list]

    def search_db_for_id(self):
        return self.query.get([getattr(self, column.name) for column in self.__table__.primary_key])

    def auto_generate_default_primary_key(self,context):
            for primary_key,i in enumerate(self.primary_key_created_from):
                if i == 0:
                    composite_primary_key = context.get_current_parameters()[primary_key]
                else:
                    composite_primary_key = composite_primary_key + ' ' + context.get_current_parameters()[primary_key]
            return (composite_primary_key).lower().replace(' ','.')
