import ENV
# Uncomment this when you start on the postgres layer
# import psycopg2
import sqlite3


class Database:
    class Table:
        def __init__(self, connection, name):
            self.connection = connection
            self.name = name
            if ENV.DATABASE == "sqlite": 
                self.columns = [i[1] for i in self.connection.cursor().execute("pragma table_info(%s)" % self.name)]
    
        def select(self, **kwargs):
            # Someday I should have a Selection object, but that's for another day
            output = []
            if not kwargs:
                output = list(self.connection.cursor().execute("select %s from %s" % (", ".join(self.columns), self.name)))
            else:
                output = list(self.connection.cursor().execute("select (%s) from table %s where %s" % (",".join(self.columns), self.name, " and ".join("%s=?" % i for i in kwargs.keys())),
                                                           (i for i in kwargs.values())))
            return [{i:j for i in self.columns for j in currLine} for currLine in output]


    def __init__(self, databaseName=None, username=None):
        if ENV.DATABASE == "pgsql":
            raise NotImplementedError("I haven't done the postgres layer yet")
        elif ENV.DATABASE == "sqlite":
            self.connection = sqlite3.connect(ENV.DB_FILE)
        else:
            raise Exception("%s isn't the name of a database I know about" % ENV.DATABASE)
    def getTable(self, tableName):
        return Database.Table(self.connection, tableName)
