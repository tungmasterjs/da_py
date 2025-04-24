import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import signup_ui
import mysql.connector


class SignupForm(QtWidgets.QDialog):
    def __init__(self,mysql_connector,main_ui, main_form):
        super().__init__()
        #Khai báo signup form
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        
        self.signup_ui = signup_ui.Ui_signup_form()
        self.signup_ui.setupUi(self)
        self.user_role = ['Admin','Tiếp tân','Quản lý']
        
        self.signup_ui.signup_btn.clicked.connect(self.handle_signup)
        self.signup_ui.role_cbx.addItems(self.user_role)
    
    
    def kiem_tra_user_id(self, user_id):
        # Kiểm tra xem số hoá đơn đã tồn tại trong dữ liệu hay không
        query_user_id = """SELECT COUNT(*) FROM user_acc WHERE user_id=%s"""
        result_user_id = self._mysql_connector.execute_query(query=query_user_id,params=(user_id,),select=True)
        return result_user_id[0][0] > 0
    
    def handle_signup(self):
        try:
            user_id = self.signup_ui.user_id_edit.text()
            user_name = self.signup_ui.user_name_edit.text()
            pass_word = self.signup_ui.password_edit.text()
            user_role = self.signup_ui.role_cbx.currentText()
            
            
            if self.kiem_tra_user_id(user_id):
                QtWidgets.QMessageBox.information(self.main_form,"Thông báo","Tên đăng nhập đã tồn tại!")
            else:
                query = """INSERT INTO user_acc (user_id,user_name,pass_word,user_role) VALUES (%s,%s,%s,%s)"""
                params = (user_id,user_name,pass_word,user_role)
                self._mysql_connector.execute_query(query=query,params=params)
                QtWidgets.QMessageBox.information(self.main_form,"Thông báo","Tạo tài khoản thành công!")
                self.main_form.show_data_user()
                self.close()
                
        except mysql.connector.Error as err:
            print(err)
            QtWidgets.QMessageBox.information(self.main_form,"Thông báo","Tạo tài khoản không thành công, vui lòng thử lại!")
            
        