import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import barber_ui
from Fourmenbarbershop_package.gui import barber_edit
from Fourmenbarbershop_package.gui import FourMenBarberShop_ui
from Fourmenbarbershop_package import FourMenBarberShop
import mysql.connector

class BarberWidget():
    def __init__(self,mysql_connector,main_ui, main_form):
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        
        #Khai báo barber form
        self.barber_form = QtWidgets.QDialog()
        self.barber_ui = barber_ui.Ui_barber_form()
        self.barber_ui.setupUi(self.barber_form)
        
        #Khai báo barber edit form
        self.barber_edit_form = QtWidgets.QDialog()
        self.barber_edit_ui = barber_edit.Ui_barber_edit_form()
        self.barber_edit_ui.setupUi(self.barber_edit_form)
        self.main_ui.ds_tho_tablewidget.itemSelectionChanged.connect(self.get_info_tho)
        
        #Gọi hàm tìm kiếm vật tư
        self.main_ui.tim_tho_btn.clicked.connect(self.tim_tho)
        self.main_ui.tim_tho_tbx.returnPressed.connect(self.main_ui.tim_tho_btn.click)
        #Hiện gợi ý, lịch sử
        self.completer = QtWidgets.QCompleter(self.hien_goi_y())
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.main_ui.tim_tho_tbx.setCompleter(self.completer)

    
    #Hàm mở đóng form thêm thợ
    def open_barber_form(self):
        self.barber_form.show()
        self.barber_ui.ma_tho_edit.setText(str(self.get_ma()))
        
        self.barber_ui.luu_them_tho_btn.clicked.connect(self.insert_tho)
        self.barber_ui.ket_thuc_them_tho_btn.clicked.connect(self.close_barber_form)
    def close_barber_form(self):
        self.barber_form.close()
        
    #Hàm mở đóng form sửa thợ
    def open_barber_edit_form(self):
        self.barber_edit_form.show()
        self.barber_edit_ui.luu_edit_tho_btn.clicked.connect(self.update_tho)
        self.barber_edit_ui.ket_thuc_edit_tho_btn.clicked.connect(self.close_barber_edit_form)
    def close_barber_edit_form(self):
        self.barber_edit_form.close()
    
    def hien_goi_y(self):
        query = "SELECT DISTINCT ma_tho, ten_tho, sdt_tho FROM Tho"
        return self.main_form.get_search_history(query=query)

    #Tìm kiếm
    def tim_tho(self):
        if self.main_ui.tim_tho_tbx.text() == '':
            self.show_data_tho()
        else:
            query = "SELECT * FROM Tho WHERE ma_tho=%s OR ten_tho=%s OR sdt_tho=%s"
            params = (self.main_ui.tim_tho_tbx.text(),self.main_ui.tim_tho_tbx.text(),self.main_ui.tim_tho_tbx.text())
            result = self._mysql_connector.execute_query(query=query,params=params,select=True)
            if result:
                self.main_ui.ds_tho_tablewidget.setRowCount(len(result))
                self.main_ui.ds_tho_tablewidget.setColumnCount(4)
                for row_index, row in enumerate(result):
                    for col_index,value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.main_ui.ds_tho_tablewidget.setItem(row_index,col_index, item)
            else:
                self.main_ui.ds_tho_tablewidget.clearContents()
                self.main_ui.ds_tho_tablewidget.setItem(0,2,QtWidgets.QTableWidgetItem("Không có kết quả"))
    
    #Show data thợ
    def show_data_tho(self):
        query = "SELECT * FROM Tho"
        result = self._mysql_connector.execute_query(query,select=True)
        if result:
            self.main_ui.ds_tho_tablewidget.setRowCount(len(result))
            self.main_ui.ds_tho_tablewidget.setColumnCount(4)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.main_ui.ds_tho_tablewidget.setItem(row_index,col_index,item)
        else:
            print("Không có data thợ")
            
    #CRUD - Thợ
    def get_ma(self):
        query = "SELECT ma_tho FROM Tho ORDER BY ma_tho DESC LIMIT 1"
        obj_type = "TH"
        byte = 3
        first_id = "001"
        ma_tho = self.main_form.generate_ma(query=query,obj_type=obj_type,byte=byte,first_id=first_id)
        return ma_tho
    #Insert - Thợ
    def insert_tho(self):
        try:
            ma_tho = self.get_ma()
            self.barber_ui.ma_tho_edit.setText(ma_tho)
            ten_tho = self.barber_ui.ten_tho_edit.text()
            sdt_tho = self.barber_ui.sdt_tho_edit.text()
            so_nam = self.barber_ui.so_nam_kn_edit.text()  
            
            query = "INSERT INTO Tho (ma_tho,ten_tho,sdt_tho,so_nam_kinh_nghiem) VALUES (%s,%s,%s,%s)"
            params = (ma_tho,ten_tho,sdt_tho,so_nam)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_tho()
            self.barber_ui.ten_tho_edit.clear()
            self.barber_ui.sdt_tho_edit.clear()
            self.barber_ui.so_nam_kn_edit.clear()
            self.barber_form.close()
            print("Insert successfully")
        except mysql.connector.Error as err:
            print(f'Lỗi: {err}')
    
    def get_info_tho(self):
        try:
            selected_items = self.main_ui.ds_tho_tablewidget.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_tho_tablewidget.currentRow()
            ma_tho = self.main_ui.ds_tho_tablewidget.item(row,0).text()
            ten_tho = self.main_ui.ds_tho_tablewidget.item(row,1).text()
            sdt_tho = self.main_ui.ds_tho_tablewidget.item(row,2).text()
            so_nam = self.main_ui.ds_tho_tablewidget.item(row,3).text()
            self.barber_edit_ui.ma_tho_edit.setText(ma_tho)
            self.barber_edit_ui.ten_tho_edit.setText(ten_tho)
            self.barber_edit_ui.sdt_tho_edit.setText(sdt_tho)
            self.barber_edit_ui.so_nam_kn_edit.setText(so_nam)
            return ma_tho
        except mysql.connector.Error as err:
            print(f'Lỗi: {err}')
            
    #Update - Thợ
    def update_tho(self):
        try:
            ma_kh = self.barber_edit_ui.ma_tho_edit.text()
            ten_tho = self.barber_edit_ui.ten_tho_edit.text()
            sdt_tho = self.barber_edit_ui.sdt_tho_edit.text()
            so_nam = self.barber_edit_ui.so_nam_kn_edit.text()
            
            query = "UPDATE Tho SET ten_tho=%s, sdt_tho=%s, so_nam_kinh_nghiem=%s WHERE ma_tho=%s"
            params = (ten_tho,sdt_tho,so_nam,ma_kh)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_tho()
            print('Update successfully')
            self.barber_edit_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
    
    #Xoá - Thợ
    def delete_tho(self):
        try:
            ma_tho = self.get_info_tho()
            
            query = "DELETE FROM Tho WHERE ma_tho = %s"
            params = (ma_tho,)
            self._mysql_connector.execute_query(query=query,params=params)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá thợ {ma_tho} không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self._mysql_connector.execute_query(query,params=params)
                self.show_data_tho()
                print("Delete successfully")
            else:
                return
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")