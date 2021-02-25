from abc import ABCMeta, abstractmethod

import motor

class User:
    def __init__(self, _id, email, username, password, status, name, surname, group, hard, soft):
        self._id = str(_id)
        self.email = email
        self.username = username
        self.password = password
        self.status = status
        self.name = name
        self.surname = surname
        self.group = group
        self.hard = hard
        self.soft = soft


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
        return User(**user)

    async def update_user(self, user_info):
        pass

    async def add_user(self, user_info):
        pass

    def __init__(self, db):
        self.__storage = db['users']


if __name__ == '__main__':
    print(1)