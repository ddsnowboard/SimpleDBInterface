import unittest
import ENV
import dbInterface
import sqlite3

class TestSqlite(unittest.TestCase):
    DATABASE_NAME = "testDatabase.db"
    ENV.DB_FILE = DATABASE_NAME
    TABLE_NAME = "testTable"
    COLUMNS = ["name", "address", "email", "phone"]
    RECORDS = [["Mel Brooks", "7270 Main Street", "mel@me.net", 1234215522],
               ["Nat King Cole", "345 Second Street", "nkc@music.biz", 2142412421],
               ["Nick Carraway", "1 Wheedle Drive", "bornCeaslessly@past.org", 2341225533]]

    def test_select_all(self):
        db = dbInterface.Database(databaseName=TestSqlite.DATABASE_NAME)
        table = db.getTable(TestSqlite.TABLE_NAME)
        selection = table.select()
        self.assertItemsEqual(selection, [{i: j for (i, j) in zip(TestSqlite.COLUMNS, currRecord)} for currRecord in TestSqlite.RECORDS])

    def test_select_some(self):
        db = dbInterface.Database(databaseName=TestSqlite.DATABASE_NAME)
        table = db.getTable(TestSqlite.TABLE_NAME)
        selection = table.select(name="Mel Brooks")
        self.assertItemsEqual(selection, [{i: j for (i, j) in zip(TestSqlite.COLUMNS, TestSqlite.RECORDS[0])}])
    
    def test_insert_row(self):
        RECORD = ["Andy Dufresne", "234 CD Street", "andy@nycorrections.gov", 1425552424]
        db = dbInterface.Database(databaseName=TestSqlite.DATABASE_NAME)
        table = db.getTable(TestSqlite.TABLE_NAME)
        table.insert(**{i:j for (i, j) in zip(TestSqlite.COLUMNS, RECORD)})
        cursor = sqlite3.connect(TestSqlite.DATABASE_NAME).cursor()
        self.assertItemsEqual(TestSqlite.RECORDS + [RECORD], list(list(i) for i in cursor.execute("select %s from %s" % (",".join(TestSqlite.COLUMNS), TestSqlite.TABLE_NAME))))
        

    def setUp(self):
        self.maxDiff = None
        cursor = sqlite3.connect(TestSqlite.DATABASE_NAME).cursor()
        cursor.execute("drop table if exists %s" % TestSqlite.TABLE_NAME)
        cursor.execute("create table %s (name varchar, address varchar, email varchar, phone real)" % TestSqlite.TABLE_NAME)
        for i in TestSqlite.RECORDS:
            cursor.execute("insert into %s (%s) VALUES (%s)" % (TestSqlite.TABLE_NAME, ",".join(TestSqlite.COLUMNS), ",".join(repr(j) for j in i)))
        cursor.connection.commit()

    def tearDown(self):
        cursor = sqlite3.connect(TestSqlite.DATABASE_NAME).cursor()
        cursor.execute("drop table %s" % TestSqlite.TABLE_NAME)
        cursor.connection.commit()


if __name__ == "__main__":
    unittest.main()
