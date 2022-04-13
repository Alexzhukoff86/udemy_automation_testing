from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):

    def test_crud(self):
        with self.app_context():
            user = UserModel(username='TestUser', password='qwerty')

            self.assertIsNone(UserModel.find_by_name('TestUser'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_name('TestUser'))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_name('TestUser'))
            self.assertIsNone(UserModel.find_by_id(1))
