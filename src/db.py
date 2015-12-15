import pymongo

from . logger import Logger

logger = Logger.logger


class Mongo(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = (super(Mongo, cls).
                             __new__(cls, *args, **kwargs))
        return cls._instance

    def __init__(self, uri="localhost"):
        try:
            self.connection = pymongo.MongoClient(uri)
            # self.connection.the_database.authenticate('admin', 'admin', mechanism='MONGODB-CR')
            # uri = "mongodb://user:password@example.com/the_database?authMechanism=MONGODB-CR"
            # self.connection = MongoClient(uri)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logger.exception("Cannot connect to server")

    def _get_database(self, database):
        return getattr(self.connection, database)

    def _get_collection(self, database, collection):
        return getattr(self._get_database(database), collection)

    def get_all_databases(self):
        logger.debug("getting all databases")
        return self.connection.database_names()

    def get_all_collections(self, database):
        logger.debug("getting all collections")
        database = getattr(self.connection, database)
        return database.collection_names()

    def get_all_documents(self, database, collection):
        logger.debug("get_all_documents")
        database = getattr(self.connection, database)
        collection = getattr(database, collection)
        return collection.find()

    def get_content(self, database, collection, filter):
        logger.debug("getting content")
        collection = self._get_collection(database, collection)
        key = collection.find()[0].keys()[0]
        return collection.find({key: filter})[0]

    def get_count(self, database, collection=None):
        logger.debug("getting count")
        database = getattr(self.connection, database)
        if collection:
            return getattr(database, collection).count()
        return len(database.collection_names())
