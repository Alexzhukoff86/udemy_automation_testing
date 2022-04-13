import hmac
from models.user import UserModel


def authenticate(username, password):
    """
    Func that gets called when a user calls the /auth endpoint
    with their username and password
    :param username: User's username
    :param password:
    :return: UserModel object if auth ok, None otherwise
    """
    user = UserModel.find_by_name(username=username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    """
    Func that gets called when user has already authed and Flask-JWT
    verified their auth header is correct
    :param payload: A dict with 'identity' key, which is the user id
    :return:
    """
    user_id = payload.get('identity')
    return UserModel.find_by_id(user_id)
