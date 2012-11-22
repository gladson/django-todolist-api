# coding: utf-8
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from todolist.models import List, Item


class ListResource(ModelResource):
    def alter_list_data_to_serialize(self, request, data):
        return data["objects"]

    def dehydrate(self, bundle):
        bundle.data['open_items'] = Item.objects.filter(
            list__id=bundle.data["id"], done=0).count()

        return bundle

    class Meta:
        queryset = List.objects.all()
        resource_name = 'lists'
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True


class ItemResource(ModelResource):
    list = fields.ForeignKey(ListResource, 'list', full=True)

    def alter_list_data_to_serialize(self, request, data):
        return data["objects"]

    class Meta:
        queryset = Item.objects.all()
        resource_name = 'items'
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True
        filtering = {
            'list': ALL,
            'done': ALL,
        }
