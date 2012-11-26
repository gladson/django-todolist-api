from django.test import TestCase
from tastypie.test import ResourceTestCase
from todolist.models import List, Item


class ListModelTest(TestCase):
    def setUp(self):
        self.list = List.objects.create(name='list name')

    def test_create(self):
        self.assertEqual(1, self.list.pk)

    def test_unicode(self):
        self.assertEqual(u'list name', unicode(self.list))


class ItemModelTest(TestCase):
    def setUp(self):
        list = List.objects.create(name='list name')
        self.item = Item.objects.create(name='item name', list=list)

    def test_create(self):
        self.assertEqual(1, self.item.pk)

    def test_unicode(self):
        self.assertEqual(u'item name', unicode(self.item))


class ListResourceTest(ResourceTestCase):
    def setUp(self):
        super(ListResourceTest, self).setUp()

        self.list = List.objects.create(name="list name")
        self.list_2 = List.objects.create(name='list name 2')

        self.item_open = Item.objects.create(name="item name", list=self.list_2)
        self.item_close = Item.objects.create(name="item name", list=self.list, done=True)

        self.post_data = {
            'name': 'list name post'
        }

    def test_get_list_json(self):
        resp = self.api_client.get('/api/v1/lists/', format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)), 2)

        self.assertEqual(self.deserialize(resp)[0], {
            'id': self.list.id,
            'name': u'list name',
            'open_items': 0
        })

    def test_list_with_item_open(self):
        resp = self.api_client.get('/api/v1/lists/%i' % self.list_2.id, format='json')

        self.assertValidJSONResponse(resp)

        self.assertEqual(self.deserialize(resp), {
            'id': self.list_2.id,
            'name': u'list name 2',
            'open_items': 1
        })

    def test_list_with_item_close(self):
        resp = self.api_client.get('/api/v1/lists/%i' % self.list.id, format='json')

        self.assertValidJSONResponse(resp)

        self.assertEqual(self.deserialize(resp), {
            'id': self.list.id,
            'name': u'list name',
            'open_items': 0
        })

    def test_post_list(self):
        self.assertEqual(List.objects.count(), 2)
        self.assertHttpCreated(self.api_client.post('/api/v1/lists/', format='json', data=self.post_data))
        self.assertEqual(List.objects.count(), 3)

    def test_put_list(self):
        url = '/api/v1/lists/%i' % self.list.id
        original_data = self.deserialize(self.api_client.get(url, format='json'))
        original_data["name"] = "list name updated"
        self.assertEqual(List.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(url, format='json', data=original_data))
        self.assertEqual(List.objects.count(), 2)
        self.assertEqual(List.objects.get(pk=self.list.id).name, u'list name updated')

    def test_delete_list(self):
        url = '/api/v1/lists/%i' % self.list.id
        self.assertEqual(List.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.delete(url, format='json'))
        self.assertEqual(List.objects.count(), 1)


class ItemResourceTest(ResourceTestCase):
    def setUp(self):
        super(ItemResourceTest, self).setUp()
        self.list = List.objects.create(name="list name")
        self.list_2 = List.objects.create(name="list name 2")
        self.item = Item.objects.create(name="item name", list=self.list)
        self.item_2 = Item.objects.create(name='item name 2', list=self.list, done=True)

        self.post_data = {
            'name': 'item name post',
            'list': {'id': self.list.id}
        }

    def test_get_item_json(self):
        resp = self.api_client.get('/api/v1/items/', format='json')
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)), 2)

        self.assertEqual(self.deserialize(resp)[0], {
            'id': self.item.id,
            'name': u'item name',
            'done': False,
            'list': {
                'id': self.list.id,
                'name': u'list name',
                'open_items': 1
            }
        })

    def test_item_filter_list(self):
        resp = self.api_client.get('/api/v1/items/', data={'format': 'json', 'list': self.list.id})
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)), 2)

    def test_item_filter_list_empty(self):
        resp = self.api_client.get('/api/v1/items/', data={'format': 'json', 'list': self.list_2.id})
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)), 0)

    def test_item_filter_done(self):
        resp = self.api_client.get('/api/v1/items/', data={'format': 'json', 'done': True})
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)), 1)

    def test_post_item(self):
        self.assertEqual(Item.objects.count(), 2)
        self.assertHttpCreated(self.api_client.post('/api/v1/items/', format='json', data=self.post_data))
        self.assertEqual(Item.objects.count(), 3)

    def test_put_list(self):
        url = '/api/v1/items/%i' % self.item.id
        original_data = self.deserialize(self.api_client.get(url, format='json'))
        self.assertEqual(original_data["done"], False)
        original_data["done"] = True
        original_data["list"] = {'id': self.list.id}
        self.assertEqual(Item.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(url, format='json', data=original_data))
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(pk=self.item.id).done, True)

    def test_delete_list(self):
        url = '/api/v1/items/%i' % self.item.id
        self.assertEqual(Item.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.delete(url, format='json'))
        self.assertEqual(Item.objects.count(), 1)
