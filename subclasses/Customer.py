import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
import mysql.connector
from Fourmenbarbershop_package.gui import customer_ui
from Fourmenbarbershop_package.gui import customer_edit_ui
from Fourmenbarbershop_package.gui import FourMenBarberShop_ui

class CustomerWidget:
    def __init__(self, mysql_connector, main_ui, main_form):
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        self._loai_kh = ['Thường','VIP']
        
        #Khai báo customer form - Mở form thêm khách hàng
        self.customer_form = QtWidgets.QDialog()
        self.customer_ui = customer_ui.Ui_customer_form()
        self.customer_ui.setupUi(self.customer_form)
        
        #Khai báo customer_edit form
        self.customer_edit_form = QtWidgets.QDialog()
        self.customer_edit_ui = customer_edit_ui.Ui_customer_edit_form()
        self.customer_edit_ui.setupUi(self.customer_edit_form)
        self.main_ui.ds_kh_tablewidget.itemSelectionChanged.connect(self.get_info_kh)
        
        #Gọi hàm tìm kiếm khách hàng
        self.main_ui.tim_kh_btn.clicked.connect(self.tim_kh)
        self.main_ui.tim_kh_tbx.returnPressed.connect(self.main_ui.tim_kh_btn.click)
        
        #Hiện gợi ý, lịch sử
        self.completer = QtWidgets.QCompleter(self.hien_goi_y())
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.main_ui.tim_kh_tbx.setCompleter(self.completer)
        
    def open_customer_form(self):
        self.customer_form.show()
        self.customer_ui.loai_kh_them_cbx.addItems(self._loai_kh)
        self.customer_ui.ma_kh_them_edit.setText(str(self.get_ma()))
        
        self.customer_ui.luu_kh_btn.clicked.connect(self.insert_kh)
        self.customer_ui.ket_thuc_kh_btn.clicked.connect(self.close_customer_form)
    def close_customer_form(self):
        self.customer_form.close()
        
    def open_customer_edit_form(self):
        self.customer_edit_form.show()
        self.customer_edit_ui.loai_kh_cbx.addItems(self._loai_kh)
        self.customer_edit_ui.luu_kh_btn.clicked.connect(self.update_kh)
        self.customer_edit_ui.ket_thuc_kh_btn.clicked.connect(self.close_customer_edit_form)
    def close_customer_edit_form(self):
        self.customer_edit_form.close()
    
    
    def hien_goi_y(self):
        query = "SELECT DISTINCT ma_kh, ten_kh, sdt_kh FROM KhachHang"
        return self.main_form.get_search_history(query=query)
    
    #Show danh sách khách hàng
    def show_data_kh(self):
        query = "SELECT * FROM KhachHang"
        result = self._mysql_connector.execute_query(query,select=True)
        if result:
            self.main_ui.ds_kh_tablewidget.setRowCount(len(result))
            self.main_ui.ds_kh_tablewidget.setColumnCount(5)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.main_ui.ds_kh_tablewidget.setItem(row_index,col_index, item)
        else:
            print("Không có data Khách hàng")
    
    def tim_kh(self):
        if self.main_ui.tim_kh_tbx.text() == '':
            self.show_data_kh()
        else:
            query = "SELECT * FROM KhachHang WHERE ma_kh=%s OR ten_kh=%s OR sdt_kh=%s"
            params = (self.main_ui.tim_kh_tbx.text(),self.main_ui.tim_kh_tbx.text(),self.main_ui.tim_kh_tbx.text())
            result = self._mysql_connector.execute_query(query=query,params=params,select=True)
            if result:
                self.main_ui.ds_kh_tablewidget.setRowCount(len(result))
                self.main_ui.ds_kh_tablewidget.setColumnCount(5)
                for row_index, row in enumerate(result):
                    for col_index,value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.main_ui.ds_kh_tablewidget.setItem(row_index,col_index, item)
            else:
                self.main_ui.ds_kh_tablewidget.clearContents()
                self.main_ui.ds_kh_tablewidget.setItem(0,2,QtWidgets.QTableWidgetItem("Không có kết quả"))
        
        
    #CRUD - Khách hàng
    def get_ma(self):
        query = ("SELECT ma_kh FROM KhachHang ORDER BY ma_kh DESC LIMIT 1")
        obj_type = "KH"
        byte = 5
        first_id = "00001"
        ma_kh = self.main_form.generate_ma(query=query,obj_type=obj_type,byte=byte,first_id=first_id)
        return ma_kh
    #Insert khách hàng
    def insert_kh(self):
        try:
            ma_kh = self.get_ma()
            self.customer_ui.ma_kh_them_edit.setText(ma_kh)
            sdt_kh = self.customer_ui.sdt_kh_them_edit.text()
            ten_kh = self.customer_ui.ten_kh_them_edit.text()
            so_lan = 1
            loai_kh = self.customer_ui.loai_kh_them_cbx.currentText()
            
            query = """INSERT INTO KhachHang (ma_kh,sdt_kh,ten_kh,so_lan_den,loai_kh) VALUES (%s,%s,%s,%s,%s)"""
            params = (ma_kh,sdt_kh,ten_kh,so_lan,loai_kh)
            self._mysql_connector.execute_query(query,params=params)
            self.show_data_kh()
            self.customer_ui.sdt_kh_them_edit.clear()
            self.customer_ui.ten_kh_them_edit.clear()
            self.customer_ui.loai_kh_them_cbx.clear()
            print("Insert successfully")
            self.customer_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
    
    def get_info_kh(self):
        try:
            selected_items = self.main_ui.ds_kh_tablewidget.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_kh_tablewidget.currentRow()
            ma_kh = self.main_ui.ds_kh_tablewidget.item(row,0).text()
            ten_kh = self.main_ui.ds_kh_tablewidget.item(row,1).text()
            sdt_kh = self.main_ui.ds_kh_tablewidget.item(row,2).text()
            so_lan = self.main_ui.ds_kh_tablewidget.item(row,3).text()
            loai_kh = self.main_ui.ds_kh_tablewidget.item(row,4).text()
            self.customer_edit_ui.ma_kh_edit.setText(ma_kh)
            self.customer_edit_ui.ten_kh_edit.setText(ten_kh)
            self.customer_edit_ui.sdt_kh_edit.setText(sdt_kh)
            self.customer_edit_ui.so_lan_edit.setText(so_lan)
            self.customer_edit_ui.loai_kh_cbx.setCurrentText(loai_kh)
            return ma_kh
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
            
    def update_kh(self):
        try:
            ma_kh = self.customer_edit_ui.ma_kh_edit.text()
            ten_kh = self.customer_edit_ui.ten_kh_edit.text()
            sdt_kh = self.customer_edit_ui.sdt_kh_edit.text()
            so_lan = self.customer_edit_ui.so_lan_edit.text()
            loai_kh = self.customer_edit_ui.loai_kh_cbx.currentText()

            query = "UPDATE KhachHang SET ten_kh=%s, sdt_kh=%s, so_lan_den=%s, loai_kh=%s WHERE ma_kh=%s"
            params = (ten_kh,sdt_kh,so_lan,loai_kh,ma_kh)
            self._mysql_connector.execute_query(query,params=params)
            self.show_data_kh()
            print('Update successfully')
            self.customer_edit_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
            
    def delete_kh(self):
        try:
            ma_kh = self.get_info_kh()
            query = "DELETE FROM KhachHang WHERE ma_kh = %s"
            params = (ma_kh,)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá khách hàng {ma_kh} không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self._mysql_connector.execute_query(query,params=params)
                self.show_data_kh()
                print("Delete successfully")
            else:
                return
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")