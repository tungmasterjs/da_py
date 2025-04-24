import mysql.connector

class MySQL_Connector:
    def __init__(self,host,username,password,database):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self.connection = None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self._host,
                username = self._username,
                password = self._password,
                database = self._database
        )
            print("Kết nối database thành công")
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Đã ngắt kết nối với database")
        else:
            print("Không có databse nào đang kết nối")
    
    def execute_query(self,query,params=None,select=False):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query,params)
                if select:
                    result = cursor.fetchall()
                    cursor.close()
                    return result
                else:
                    self.connection.commit()
                    cursor.close()
            except mysql.connector.Error as err:
                print(f"Lỗi: {err}")
                return None 
        else: 
            print("Không có database nào đang kết nối")
    
    def execute_many_query(self,query,params=None,select=False):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.executemany(query,params)
                if select:
                    result = cursor.fetchall()
                    cursor.close()
                    return result
                else:
                    self.connection.commit()
                    cursor.close()
            except mysql.connector.Error as err:
                print(f"Lỗi: {err}")
                return None 
        else: 
            print("Không có database nào đang kết nối")
                