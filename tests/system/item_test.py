import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                user = UserModel(username='testUser', password='qwerty')
                user.save_to_db()
                auth_r = c.post('/auth', json={'username': f'{user.username}',
                                               'password': f'{user.password}'
                                               })
                self.auth_token = json.loads(auth_r.data).get('access_token')
                self.header = {'Authorization': f'JWT {self.auth_token}'}

    def test_get_item_no_auth(self):
        with self.app() as c:
            with self.app_context():
                ItemModel(name='testStore', price=19.99, store_id=1).save_to_db()
                r = c.get(f'/item/testItem')
                self.assertEqual(401, r.status_code)
                self.assertDictEqual({'message': 'Could not authorize.'}, json.loads(r.data))

    def test_get_item_not_found(self):
        with self.app() as c:
            with self.app_context():
                r = c.get(f'/item/test', headers=self.header)
                self.assertEqual(404, r.status_code)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(r.data))

    def test_get_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.get(f'/item/testItem', headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({
                    'name': 'testItem',
                    'price': 19.99
                }, json.loads(r.data))

    def test_create_items(self):
        with self.app() as c:
            with self.app_context():
                item = ItemModel(name='testItme', price=19.99, store_id=1)
                r = c.post(f'/item/{item.name}', json={
                    'price': item.price,
                    'store_id': item.store_id
                }, headers=self.header)
                expected = {
                    'name': f'{item.name}',
                    'price': item.price
                }
                self.assertEqual(201, r.status_code)
                self.assertDictEqual(expected, json.loads(r.data))

    def test_create_duplicate(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.post(f'/item/testItem', json={
                    'price': 19.99,
                    'store_id': 1
                }, headers=self.header)
                self.assertEqual(400, r.status_code)
                expected = {'message': "An item with name 'testItem' already exists."}
                self.assertDictEqual(expected, json.loads(r.data))

    def test_delete_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.delete('/item/testItem', headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(r.data))

    def test_put_non_existed_item(self):
        with self.app() as c:
            with self.app_context():
                r = c.put('/item/testItem', json={'price': 19.99, 'store_id': 1},
                          headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({
                    'name': 'testItem', 'price': 19.99
                }, json.loads(r.data))
                self.assertEqual(ItemModel.find_by_name('testItem').price, 19.99)

    def test_update_existed_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.put(f'/item/testItem', json={
                    'price': 29.99,
                    'store_id': 1
                }, headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({
                    'name': 'testItem',
                    'price': 29.99}, json.loads(r.data))
                self.assertEqual(ItemModel.find_by_name('testItem').price, 29.99)

    def test_get_item_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                ItemModel(name='testItem', price=19.99, store_id=1).save_to_db()
                r = c.get(f'/items', headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'items': [
                    {
                        'name': 'testItem',
                        'price': 19.99
                    }
                ]}, json.loads(r.data))

    def test_get_empty_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel(name='testStore').save_to_db()
                r = c.get(f'/items', headers=self.header)
                self.assertEqual(200, r.status_code)
                self.assertDictEqual({'items': []}, json.loads(r.data))
