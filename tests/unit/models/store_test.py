from unittest import TestCase

from models.store import StoreModel


class StoreTest(TestCase):

    def setUp(self) -> None:
        self.store = StoreModel(name='Test')

    def test_new_store(self):
        self.assertEqual('Test', self.store.name)
