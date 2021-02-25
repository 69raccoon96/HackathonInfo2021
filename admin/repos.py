from abc import ABCMeta, abstractmethod

from bson import ObjectId


class AbstractAdminEntityRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_list(self, amount, page):
        pass

    @abstractmethod
    async def find_by_id(self, idx):
        pass

    @abstractmethod
    async def find(self, amount, **kwargs):
        pass

    @abstractmethod
    async def add(self, entity):
        pass

    @abstractmethod
    async def remove(self, idx):
        pass

    @abstractmethod
    async def update(self, idx, **kwargs):
        pass


class MongoAdminUserRepository(AbstractAdminEntityRepository):
    async def get_list(self, amount=100, page=0):
        collection = self.__storage.find()
        ulist = await collection.skip(amount*page).to_list(amount)
        res = {'users': ulist}
        if len(ulist) >= amount:
            res['next_page'] = page+1
        return res

    def __init__(self, db):
        self.__storage = db['users']

    async def find_by_id(self, idx):
        return await self.__storage.find_one({"_id": ObjectId(idx)})

    async def find(self, amount=100, **kwargs):
        collection = self.__storage.find(kwargs)
        ulist = await collection.to_list(amount)
        return ulist

    async def add(self, entity):
        inserted = await self.__storage.insert_one(entity)
        idx = inserted.inserted_id
        return await self.find_by_id(str(idx))

    async def remove(self, idx):
        await self.__storage.delete_one({'_id': ObjectId(idx)})

    async def update(self, idx, **kwargs):
        await self.__storage.update_one({'_id': ObjectId(idx)}, kwargs)


class MongoAdminCourseRepository(AbstractAdminEntityRepository):
    def __init__(self, db):
        self.__storage = db['courses']

    async def get_list(self, amount=100, page=0):
        collection = self.__storage.find()
        ulist = await collection.skip(amount * page).to_list(amount)
        print(ulist)
        res = {'courses': ulist}
        if len(ulist) >= amount:
            res['next_page'] = page + 1
        return res

    async def find_by_id(self, idx):
        return await self.__storage.find_one({"_id": ObjectId(idx)})

    async def find(self, amount=100, **kwargs):
        collection = self.__storage.find(kwargs)
        ulist = await collection.to_list(amount)
        return ulist

    async def add(self, entity):
        inserted = await self.__storage.insert_one(entity)
        idx = inserted.inserted_id
        return await self.find_by_id(str(idx))

    async def remove(self, idx):
        await self.__storage.delete_one({'_id': ObjectId(idx)})

    async def update(self, idx, **kwargs):
        await self.__storage.update_one({'_id': ObjectId(idx)}, kwargs)


class MongoAdminSubjectRepository(AbstractAdminEntityRepository):
    def __init__(self, db):
        self.__storage = db['subjects']

    async def get_list(self, amount=100, page=0):
        collection = self.__storage.find()
        ulist = await collection.skip(amount * page).to_list(amount)
        print(ulist)
        res = {'subjects': ulist}
        if len(ulist) >= amount:
            res['next_page'] = page + 1
        return res

    async def find_by_id(self, idx):
        return await self.__storage.find_one({"_id": ObjectId(idx)})

    async def find(self, amount=100, **kwargs):
        collection = self.__storage.find(kwargs)
        ulist = await collection.to_list(amount)
        return ulist

    async def add(self, entity):
        inserted = await self.__storage.insert_one(entity)
        idx = inserted.inserted_id
        return await self.find_by_id(str(idx))

    async def remove(self, idx):
        await self.__storage.delete_one({'_id': ObjectId(idx)})

    async def update(self, idx, **kwargs):
        await self.__storage.update_one({'_id': ObjectId(idx)}, kwargs)