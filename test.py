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
        self.assertItemsEqual(selection, [{i: j for i in TestSqlite.COLUMNS for j in currRecord} for currRecord in TestSqlite.RECORDS])

    def setUp(self):
        cursor = sqlite3.connect(TestSqlite.DATABASE_NAME).cursor()
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
