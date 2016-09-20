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
            inputString = "select %s from %s" % (", ".join(self.columns), self.name)
            output = []
            if not kwargs:
                output = list(self.connection.cursor().execute(inputString))
            else:
                inputString = "%s where %s" % (inputString, " and ".join("%s=?" % i for i in kwargs.keys()))
                output = list(self.connection.cursor().execute("select %s from %s where %s" % (",".join(self.columns), self.name, " and ".join("%s=?" % i for i in kwargs.keys())),
                                                           [i for i in kwargs.values()]))
            ret = [{i:j for i, j in zip(self.columns, currLine)} for currLine in output]
            return ret
        
        def insert(self, **kwargs):
            for col in self.connection.cursor().execute("pragma table_info(%s)" % self.name):
                id, name, type, notnull, default, pk = col
                if not name in kwargs.keys():
                    if notnull:
                        raise Exception("You have to pass in a value for %s! It can't be null!" % name)

            self.connection.cursor().execute("insert into %s (%s) VALUES (%s)" % (self.name, ",".join(kwargs.keys()), ",".join("?" for i in kwargs.keys())), 
                                             kwargs.values())
            self.connection.commit()

    def __init__(self):
        if ENV.DATABASE == "pgsql":
            raise NotImplementedError("I haven't done the postgres layer yet")
        elif ENV.DATABASE == "sqlite":
            self.connection = sqlite3.connect(ENV.DB_FILE)
        else:
            raise Exception("%s isn't the name of a database I know about" % ENV.DATABASE)
    def getTable(self, tableName):
        return Database.Table(self.connection, tableName)

def createTable(name, *cols):
    if not reduce(lambda x, y: x and type(y) == type({}), cols):
        raise Exception("You didn't give dictionaries for the columns!")
    connection = sqlite3.connect(ENV.DB_FILE)
    i = cols[0]
    query = "create table %s (%s)" % (name, ",".join("%s %s %s" % (i["name"], i["type"], "not null" if not i.get("null", True) else "") for i in cols))
    connection.cursor().execute(query)
    connection.commit()
