import sys
sys.path.append('../DO AN')
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from Fourmenbarbershop_package.subclasses import Customer
from Fourmenbarbershop_package.subclasses.Login import LoginForm
from Fourmenbarbershop_package.subclasses.Signup import SignupForm
from Fourmenbarbershop_package.subclasses import Barber
from Fourmenbarbershop_package.subclasses import Booking
from Fourmenbarbershop_package.subclasses import Inventory
from Fourmenbarbershop_package.subclasses import Booking
from Fourmenbarbershop_package.subclasses import Bill
from Fourmenbarbershop_package.subclasses import Statistics
from Fourmenbarbershop_package.subclasses import Payment
from Fourmenbarbershop_package.gui.FourMenBarberShop_ui import Ui_MainWindow
from Fourmenbarbershop_package.MySQL_connector import MySQL_Connector
import mysql.connector

class FourMenBarberShop(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mysql_connector =   MySQL_Connector(
            host = '127.0.0.1',
            username = 'root',
            password= 'admin',
            database='4MEN_BARBERSHOP'
        )
        self.mysql_connector.connect()
        self.user_role = ['Admin','Tiếp tân','Quản lý']
        
        #Khai báo main window
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        
        self.login_form = LoginForm()
        self.login_ui = self.login_form.login_ui
        self.signup_form = SignupForm(self.mysql_connector,self.main_ui, self)
        
        self.login_ui.login_btn.clicked.connect(self.handle_login)
        
        #Mở widget mặc định
        self.main_ui.stackedWidget_2.setCurrentWidget(self.main_ui.welcome_form)
        self.init_widgets()
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.thongke_page)
        
        self.main_ui.quan_ly_tiem_act.triggered.connect(self.handle_main)
        self.main_ui.phan_quyen_act.triggered.connect(self.handle_role)
        self.main_ui.doi_mk_act.triggered.connect(self.handle_change_pw)
        self.main_ui.dang_xuat_act.triggered.connect(self.handle_logout)
        self.main_ui.ket_thuc_act.triggered.connect(self.handle_exit)
        
        self.login_form.show()
        self.show_connection()

    
    def init_widgets(self):
        #Khai báo form thống kê
        self.statistics_widget = Statistics.StatisticsWidget(self.mysql_connector,self.main_ui,self)
        #Khai báo form khách hàng
        self.customer_wid = Customer.CustomerWidget(self.mysql_connector,self.main_ui, self)
        self.customer_wid.show_data_kh()
        #Khai báo form thợ
        self.barber_wid = Barber.BarberWidget(self.mysql_connector,self.main_ui,self)
        self.barber_wid.show_data_tho()
        #Khai báo form vật tư
        self.inventory_widget = Inventory.InventoryWidget(self.mysql_connector,self.main_ui,self)
        self.inventory_widget.show_data_vattu()
        #Khai báo form vật tư
        self.booking_widget = Booking.BookingWidget(self.mysql_connector,self.main_ui,self)
        self.booking_widget.show_data_lichhen()
        #Khai báo form thanh toán
        self.payment_widget = Payment.PaymentWidget(self.mysql_connector,self.main_ui,self)
        #Khai báo bill form
        self.bill_widget = Bill.BillWidget(self.mysql_connector,self.main_ui,self)
        self.bill_widget.show_data_hd()
        
        #Kết nối button gọi form khách hàng
        self.main_ui.them_kh_btn.clicked.connect(self.customer_wid.open_customer_form)
        self.main_ui.sua_kh_btn.clicked.connect(self.customer_wid.open_customer_edit_form)
        self.main_ui.xoa_kh_btn.clicked.connect(self.customer_wid.delete_kh)
        #Kết nói button gọi form thợ
        self.main_ui.them_tho_btn.clicked.connect(self.barber_wid.open_barber_form)
        self.main_ui.sua_tho_btn.clicked.connect(self.barber_wid.open_barber_edit_form)
        self.main_ui.xoa_tho_btn.clicked.connect(self.barber_wid.delete_tho)
        #Kết nói button gọi form vật tư
        self.main_ui.them_vattu_btn.clicked.connect(self.inventory_widget.open_inventory_form)
        self.main_ui.sua_vattu_btn.clicked.connect(self.inventory_widget.open_inventory_edit_form)
        self.main_ui.xoa_vattu_btn.clicked.connect(self.inventory_widget.delete_vt)
        #Kết nói button gọi form lịch hẹn
        self.main_ui.them_lich_btn.clicked.connect(self.booking_widget.open_booking_form)
        self.main_ui.sua_lich_btn.clicked.connect(self.booking_widget.open_booking_edit_form)
        self.main_ui.xoa_lich_btn.clicked.connect(self.booking_widget.delete_dl)
        #Kết nói button gọi form hoá đơn
        self.main_ui.ds_hd_btn.clicked.connect(self.bill_widget.open_bill_form)

    #Hàm nút gọi mở - đóng
    def show_connection(self):
        #Mở các widget trên cửa sổ chính
        self.main_ui.thongke_btn.clicked.connect(self.showpage_thongke)
        self.main_ui.thanhtoan_btn.clicked.connect(self.showpage_thanhtoan)
        self.main_ui.lichhen_btn.clicked.connect(self.showpage_lichhen)
        self.main_ui.khachhang_btn.clicked.connect(self.showpage_khachhang)
        self.main_ui.tho_btn.clicked.connect(self.showpage_tho)
        self.main_ui.vattu_btn.clicked.connect(self.showpage_vattu)
    
    def show_data_user(self):
        query = """SELECT user_name, user_id, user_role FROM user_acc"""
        result = self.mysql_connector.execute_query(query,select=True)
        if result:
            self.main_ui.ds_user_tb.setRowCount(len(result))
            self.main_ui.ds_user_tb.setColumnCount(3)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.main_ui.ds_user_tb.setItem(row_index,col_index, item) 
    
    def get_info_user(self):
        try:
            self.main_ui.role_cbx.addItems(self.user_role)
            selected_items = self.main_ui.ds_user_tb.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_user_tb.currentRow()
            user_name = self.main_ui.ds_user_tb.item(row,0).text()
            user_id = self.main_ui.ds_user_tb.item(row,1).text()
            user_role = self.main_ui.ds_user_tb.item(row,2).text()
            
            query = """SELECT pass_word FROM user_acc WHERE user_id=%s"""
            result = self.mysql_connector.execute_query(query,params=(user_id,),select=True)
            if result:
                pass_word = result[0][0]
            self.main_ui.user_id_edit.setText(user_id)
            self.main_ui.user_name_edit.setText(user_name)
            self.main_ui.password_edit.setText(pass_word)
            self.main_ui.role_cbx.setCurrentText(user_role)
        except mysql.connector.Error as err:
            print(err)
    
    def update_user(self):
        try:
            user_id = self.main_ui.user_id_edit.text()
            user_name = self.main_ui.user_name_edit.text()
            pass_word = self.main_ui.password_edit.text()
            user_role = self.main_ui.role_cbx.currentText()
            query = """UPDATE user_acc SET user_name=%s,pass_word=%s,user_role=%s WHERE user_id=%s"""
            params = (user_name,pass_word,user_role,user_id)
            self.mysql_connector.execute_query(query=query,params=params)
            QtWidgets.QMessageBox.information(None, "Thông báo","Cập nhật tài khoản thành công")
            self.show_data_user()
        except:
            QtWidgets.QMessageBox.warning(None, "Thông báo","Cập nhật tài khoản không thành công, vui lòng thử lại sau!")
    
    def delete_user(self):
        try:
            selected_items = self.main_ui.ds_user_tb.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_user_tb.currentRow()
            user_id = self.main_ui.ds_user_tb.item(row,1).text()
            query = "DELETE FROM user_acc WHERE user_id = %s"
            params = (user_id,)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá người dùng {user_id} không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self.mysql_connector.execute_query(query,params=params)
                self.show_data_user()
                QtWidgets.QMessageBox.information(None, "Thông báo","Xoá thành công!")
            else:
                return
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.warning(None, "Thông báo","Xoá người dùng không thành công, vui lòng thử lại sau!")
    
    #Các hàm gọi widget tương ứng trên mainwindow
    def showpage_thongke(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.thongke_page)
    def showpage_thanhtoan(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.thanh_toan_page)
    def showpage_lichhen(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.lich_hen_page)
    def showpage_khachhang(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.khach_hang_page)
    def showpage_tho(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.tho_page)
    def showpage_vattu(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.vat_tu_page)

    def handle_login(self):
        userid = self.login_ui.user_name_edit.text()
        password = self.login_ui.password_edit.text()
        query = """SELECT user_name, pass_word, user_role FROM user_acc WHERE user_id=%s"""
        result = self.mysql_connector.execute_query(query,params=(userid,),select=True)
        if result:
            if password == result[0][1]:
                self.show()
                self.login_form.close()
                user_name = result[0][0]
                user_role = result[0][2]
                self.main_ui.username_lb.setText(user_name)
                self.check_user_role(user_role)
            else:
                QtWidgets.QMessageBox.warning(None, "Lỗi đăng nhập","Mật khẩu không đúng. Vui lòng thử lại.")
        else:
            QtWidgets.QMessageBox.warning(None, "Lỗi đăng nhập","Tài khoản không đúng. Vui lòng thử lại.")
    
    def check_user_role(self, user_role):
        if user_role == 'Admin':
            # Admin có thể truy cập tất cả các chức năng
            self.main_ui.thongke_btn.setVisible(True)
            self.main_ui.thanhtoan_btn.setVisible(True)
            self.main_ui.lichhen_btn.setVisible(True)
            self.main_ui.khachhang_btn.setVisible(True)
            self.main_ui.tho_btn.setVisible(True)
            self.main_ui.vattu_btn.setVisible(True)
            self.main_ui.phan_quyen_act.setVisible(True)
        elif user_role == 'Quản lý':
            # Quản lý có thể truy cập tất cả các chức năng, trừ quản lý người dùng
            self.main_ui.thongke_btn.setVisible(True)
            self.main_ui.thanhtoan_btn.setVisible(True)
            self.main_ui.lichhen_btn.setVisible(True)
            self.main_ui.khachhang_btn.setVisible(True)
            self.main_ui.tho_btn.setVisible(True)
            self.main_ui.vattu_btn.setVisible(True)
            self.main_ui.phan_quyen_act.setVisible(False)
        elif user_role == 'Tiếp tân':
            # Tiếp tân chỉ có thể truy cập các chức năng đặt lịch hẹn, thanh toán và thống kê
            self.main_ui.thongke_btn.setVisible(True)
            self.main_ui.thanhtoan_btn.setVisible(True)
            self.main_ui.lichhen_btn.setVisible(True)
            self.main_ui.khachhang_btn.setVisible(False)
            self.main_ui.tho_btn.setVisible(False)
            self.main_ui.vattu_btn.setVisible(False)
            self.main_ui.phan_quyen_act.setVisible(False)
            self.bill_widget.bill_ui.xoa_hd_btn.setVisible(False)           
            
    def handle_signup(self):
        pass
    def open_signup_form(self):
        pass
    
    def handle_main(self):
        self.main_ui.stackedWidget_2.setCurrentWidget(self.main_ui.manage_form)
    
    def handle_role(self):
        self.show_data_user()
        self.main_ui.stackedWidget_2.setCurrentWidget(self.main_ui.phan_quyen_wid)
        self.main_ui.them_user_btn.clicked.connect(self.signup_form.show)
        self.main_ui.ds_user_tb.selectedItems
        self.main_ui.sua_user_btn.clicked.connect(self.get_info_user)
        self.main_ui.luu_user_btn.clicked.connect(self.update_user)
        self.main_ui.xoa_user_btn.clicked.connect(self.delete_user)
        
    
    def handle_change_pw(self):
        pass
    
    def handle_exit(self):
        self.close()
    
    def handle_logout(self):
        self.close()
        self.main_ui.stackedWidget_2.setCurrentWidget(self.main_ui.welcome_form)
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.thongke_page)
        self.login_form.show()
        self.login_ui.password_edit.clear()
        self.login_ui.user_name_edit.clear()
    
     
    #Hiện gợi ý tìm kiếm
    def get_search_history(self,query):
        result = self.mysql_connector.execute_query(query=query, select=True)
        history = []
        for record in result:
            history.extend(record)
        return history
    
    #Tạo mã
    def generate_ma(self,query,obj_type,byte,first_id):
        result = self.mysql_connector.execute_query(query,select=True)
        if result:
            last_ma = result[0][0]
            last_number = int(last_ma[2:])
            new_number = last_number + 1
            new_ma = obj_type+str(new_number).zfill(byte)
            return new_ma
        else:
            return str(obj_type+first_id)
    
    #Canh giữa item   
    def create_centered_item(self,text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item
    
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = FourMenBarberShop()
    sys.exit(app.exec_())


