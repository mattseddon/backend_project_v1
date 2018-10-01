"""
central location to add all db wide customisations that will not be applied to all dbs within the system
this mixin should be added to all ORMs (Object Relational Mappers)
"""
class CRMMixin():
    __bind_key__ = 'CRM'


