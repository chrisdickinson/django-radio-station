import simplerest
from simplerest.interface import RestInterface
from simplerest.authentication import logged_in
from models import *
class DJInterface(RestInterface):
    name = 'djs'
    model = DJ
    authentication = logged_in
    queryable_fields = ['pk', 'name', 'account']
    return_fields = ['pk', 'first_name', 'last_name', 'username']
    allowed_queries = ['exact', 'contains', 'startswith']
    paginate = 60
    def get_first_name(self, obj, iface):
        return obj.get_first_name()

    def get_last_name(self, obj, iface):
        return obj.get_last_name()

    def get_username(self, obj, iface):
        return obj.account.username

    def get_authentication(self):
        return logged_in
    
class ShowInterface(RestInterface):
    name = 'shows'
    model = Show
    queryable_fields = ['pk', 'name']
    return_fields = ['pk', 'name']
    allowed_queries = ['exact', 'contains', 'startswith']
    paginate = 60 
    def get_authentication(self):
        return logged_in
simplerest.root.register(DJInterface)
simplerest.root.register(ShowInterface)

