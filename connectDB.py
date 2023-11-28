import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "P@$$vv0rd",
    "database": "diemdb",
}

class MySqlDB_connect:
    def __init__(self):
        self.db = mysql.connector.connect(**db_config)
    
    def getAccountInfo(self, account):
        cursor = self.db.cursor(dictionary=True)
        query = f"SELECT * FROM taikhoan WHERE Account='{account}';"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def createAnAccount(self, account):
        cursor = self.db.cursor()
        query = f"INSERT INTO taikhoan (Id, Account, Spice, `Spice&Password`) VALUES (%s, %s, %s, %s);"
        try:
            cursor.execute(query, account)
            self.db.commit()
            cursor.close()
            return True
        except Exception:
            cursor.close()
            return False
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    db = MySqlDB_connect()
    db.getAccountInfo(4)
    db.close()