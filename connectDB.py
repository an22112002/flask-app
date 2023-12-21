import mysql.connector

class MySqlDB_connect:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "P@$$vv0rd",
            "database": "diemdb",
        }
        #self.db = mysql.connector.connect(**self.db_config)
        self.query = ""
        self.data = None
        self.success = True
    
    def execute(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(self.query)
            self.data = cursor.fetchall()
            self.success = True
        except mysql.connector.Error as err:
            print("Lỗi MySQL: {}".format(err))
            self.success = False
        finally:
            if connection.is_connected():
                connection.commit()
                cursor.close()
                connection.close()
    
    def getAccountInfo(self, account):
        self.query = f"SELECT * FROM taikhoan WHERE Account='{account}';"
        self.data = None
        self.execute()
        return self.data
    
    def getEducationProgram(self, id):
        self.query = f'''SELECT Id_chuongTrinh,TenChuongTrinh,TongTinChi FROM diemdb.chuongtrinh WHERE Id_user="{id}";'''
        self.data = None
        self.execute()
        return self.data
    
    def getSectionScore(self, id):
        self.query = f'''SELECT * FROM diemdb.diemhocphan WHERE Id_ChuongTrinh="{id}";'''
        self.data = None
        self.execute()
        return self.data
    
    def createAnAccount(self, account):
        self.query = "INSERT INTO taikhoan (Id, Account, Spice, `Spice&Password`) VALUES ('%s', '%s', '%s', '%s');" % account
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def addNewSectionScore(self, new_score):
        self.query = "INSERT INTO `diemdb`.`diemhocphan` (`Id_HocPhan`, `Id_ChuongTrinh`, `TenMon`, `SoTinChi`, `TiLeTX`, `TiLeDiem`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % new_score
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def addNewEducationProgram(self, new_program):
        self.query = "INSERT INTO `diemdb`.`chuongtrinh` (`Id_chuongTrinh`, `TenChuongTrinh`, `TongTinChi`, `Id_user`) VALUES ('%s', '%s', '%s', '%s');" % new_program
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def deleteEducationProgram(self, id):
        self.query = "DELETE FROM `diemdb`.`diemhocphan` WHERE (`Id_ChuongTrinh` = '%s');" % id
        self.execute()
        s1 = self.success
        self.query = "DELETE FROM `diemdb`.`chuongtrinh` WHERE (`Id_chuongTrinh` = '%s');" % id
        self.execute()
        s2 = self.success
        if s1 and s2:
            return True
        else:
            return False
        
    def deleteSectionScore(self, id):
        self.query = "DELETE FROM `diemdb`.`diemhocphan` WHERE (`Id_HocPhan` = '%s');" % id
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def updateSectionScore(self, value):
        self.query = "UPDATE `diemdb`.`diemhocphan` SET `Tx1` = '%s', `Tx2` = '%s', `Tx3` = '%s', `Tx4` = '%s', `Tx5` = '%s', `GiuaKy` = '%s', `CuoiKy` = '%s', `ChuyenCan` = '%s' WHERE (`Id_HocPhan` = '%s');" % value
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def changePassword(self, value):
        self.query = "UPDATE `diemdb`.`taikhoan` SET `Spice` = '%s', `Spice&Password` = '%s' WHERE (`Id` = '%s');" %  value
        self.execute()
        if self.success:
            return True
        else:
            return False
        
    def haveID_user(self, id):
        self.query = "SELECT Id FROM diemdb.taikhoan WHERE Id='%s';" % id
        self.execute()
        if (len(self.data)==0):
            return False
        return True
    
    def haveID_program(self, id):
        self.query = "SELECT Id_chuongTrinh FROM diemdb.chuongtrinh WHERE Id_chuongTrinh='%s';" % id
        self.execute()
        if (len(self.data)==0):
            return False
        return True
    
    def haveID_score(self, id):
        self.query = "SELECT Id_HocPhan FROM diemdb.diemhocphan WHERE Id_HocPhan='%s';" % id
        self.execute()
        if (len(self.data)==0):
            return False
        return True

if __name__ == "__main__":
    db = MySqlDB_connect()
    print(db.getSectionScore("#>ah]AhM&)"))