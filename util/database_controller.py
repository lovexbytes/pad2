import pymongo
from config.database_config import DatabaseConfig

class DatabaseController:
    def __init__(self):
        self.__conn = None
        
    def get_connection(self):
        if not self.__conn:
            self.__conn = pymongo.MongoClient(DatabaseConfig.MONGO_STR)[DatabaseConfig.DBNAME][DatabaseConfig.COLLECTION_NAME]
        return self.__conn
