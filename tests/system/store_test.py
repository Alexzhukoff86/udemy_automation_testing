import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):

    def test_create_store(self):
        with self.app() as c:
            with self.app_context():
                s = StoreModel('testStore')
                r = c.post(f'/store/{s.name}')
                self.assertEqual(201, r.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('testStore'))
                self.assertDictEqual(json.loads(r.data), {'items': [], 'name': 'testStore'})

    def test_create_duplicate_store(self):
        with self.app() as c:
            with self.app_context():
                s = StoreModel('testStore')
                c.post(f'/store/{s.name}')
                r = c.post(f'/store/{s.name}')
                self.assertEqual(400, r.status_code)
                self.assertDictEqual({'message': f'A store with name "{s.name}" already exists.'},
                                     json.loads(r.data))

    def test_delete_store(self):
        with self.app() as c:
            with self.app_context():
                s = StoreModel('testStore')
                c.post(f'/store/{s.name}')
                r = c.delete(f'/store/{s.name}')
                self.assertEqual(200, r.status_code)
                self.assertIsNone(StoreModel.find_by_name('testStore'))

    def test_find_store(self):
        with self.app() as c:
            with self.app_context():
                s = StoreModel('testStore')
                c.post(f'/store/{s.name}')
                r = c.get(f'/store/{s.name}')
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'name': 'testStore', 'items': []}, json.loads(r.data))

    def test_store_not_found(self):
        with self.app() as c:
            with self.app_context():
                s = StoreModel('testStore')
                r = c.get(f'/store/{s.name}')
                self.assertEqual(404, r.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(r.data))

    def test_store_found_with_items(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.get(f'/store/testStore')
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'name': 'testStore',
                                      'items':
                                          [
                                              {
                                                  'name': 'testItem',
                                                  'price': 19.99
                                              }
                                          ]}, json.loads(r.data))

    def test_store_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore1').save_to_db()
                StoreModel(name='testStore2').save_to_db()
                r = c.get(f'/stores')
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'stores': [
                    {
                        'name': 'testStore1',
                        'items': []
                    },
                    {
                        'name': 'testStore2',
                        'items': []
                    }
                ]}, json.loads(r.data))

    def test_store_list_with_items(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.get(f'/stores')
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({
                    'stores': [
                        {
                            'name': 'testStore',
                            'items': [
                                {
                                    'name': 'testItem',
                                    'price': 19.99
                                }
                            ]
                        }
                    ]
                }, json.loads(r.data))
