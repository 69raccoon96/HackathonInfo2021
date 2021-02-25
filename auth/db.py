from abc import ABCMeta, abstractmethod

import motor

class User:
    def __init__(self, **kwargs):
        self._id = str(kwargs["_id"])
        self.email = kwargs["email"]
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.status = kwargs["status"]
        self.name = kwargs["name"]
        self.surname = kwargs["surname"]
        self.group = kwargs["group"]
        self.hard = kwargs["hard"]
        self.soft = kwargs["soft"]


class AbstractUserRepository(metaclass=ABCMeta):

    @abstractmethod
    async def get_user_by_id(self, id):
        pass

    @abstractmethod
    async def get_user_by_username(self, username):
        pass

    @abstractmethod
    async def update_user(self, userinfo):
        pass

    @abstractmethod
    async def add_user(self, userinfo):
        pass


class MongoUserRepository(AbstractUserRepository):
    async def get_user_by_id(self, idx):
        pass

    async def get_user_by_username(self, username):
        user = await self.__storage.find_one({"username": username})
        if user is not None:
            return User(**user)
        else:
            return None

    async def update_user(self, user_info):
        pass

    async def add_user(self, user_info):
        pass

    def __init__(self, db):
        self.__storage = db['users']


if __name__ == '__main__':
    print(1)