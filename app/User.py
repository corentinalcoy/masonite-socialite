"""User Model."""

from config.database import Model


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password', 'provider', 'access_token']

    __auth__ = 'email'
