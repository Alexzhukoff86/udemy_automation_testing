from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):

    def test_create_user(self):
        user = UserModel(username='TestUser', password='123456')
        self.assertEqual('TestUser', user.username)
        self.assertEqual('123456', user.password)
