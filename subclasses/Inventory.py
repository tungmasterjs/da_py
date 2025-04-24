import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import inventory_ui
from Fourmenbarbershop_package.gui import inventory_edit_ui
from Fourmenbarbershop_package.gui import FourMenBarberShop_ui
import mysql.connector

class InventoryWidget:
    def __init__(self,mysql_connector,main_ui,main_form):
        super().__init__()
        self.main_ui = main_ui
        self.main_form = main_form
        self._mysql_connector = mysql_connector
        #vtai báo inventory form
        self.inventory_form = QtWidgets.QDialog()
        self.inventory_ui = inventory_ui.Ui_inventory_form()
        self.inventory_ui.setupUi(self.inventory_form)
        
        #vtai báo inventory_edit form
        self.inventory_edit_form = QtWidgets.QDialog()
        self.inventory_edit_ui = inventory_edit_ui.Ui_inventory_edit_form()
        self.inventory_edit_ui.setupUi(self.inventory_edit_form)
        self.main_ui.ds_vattu_tablewidget.itemSelectionChanged.connect(self.get_info_vt)
    
    #Gọi hàm tìm kiếm vật tư
        self.main_ui.tim_vt_btn.clicked.connect(self.tim_vt)
        self.main_ui.tim_vt_tbx.returnPressed.connect(self.main_ui.tim_vt_btn.click)
    #Hiện gợi ý, lịch sử
        self.completer = QtWidgets.QCompleter(self.hien_goi_y())
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.main_ui.tim_vt_tbx.setCompleter(self.completer)
        
    #Hàm mở đóng form thêm vật tư
    def open_inventory_form(self):
        self.inventory_form.show()
        self.inventory_ui.ma_vt_edit.setText(self.get_ma())
        self.inventory_ui.luu_vt_btn.clicked.connect(self.insert_vt)
        self.inventory_ui.ket_thuc_vt_btn.clicked.connect(self.close_inventory_form)
    def close_inventory_form(self):
        self.inventory_form.close()
    
    #Hàm mở đóng form sửa vật tư
    def open_inventory_edit_form(self):
        self.inventory_edit_form.show()
        self.inventory_edit_ui.luu_vt_btn.clicked.connect(self.update_vt)
        self.inventory_edit_ui.ket_thuc_vt_btn.clicked.connect(self.close_inventory_edit_form)
    def close_inventory_edit_form(self):
        self.inventory_edit_form.close()
    
    def hien_goi_y(self):
        query = "SELECT DISTINCT ma_vt, ten_vt FROM VatTu"
        return self.main_form.get_search_history(query=query)

    #Tìm kiếm
    def tim_vt(self):
        if self.main_ui.tim_vt_tbx.text() == '':
            self.show_data_vattu()
        else:
            query = "SELECT * FROM VatTu WHERE ma_vt=%s OR ten_vt=%s"
            params = (self.main_ui.tim_vt_tbx.text(),self.main_ui.tim_vt_tbx.text())
            result = self._mysql_connector.execute_query(query=query,params=params,select=True)
            if result:
                self.main_ui.ds_vattu_tablewidget.setRowCount(len(result))
                self.main_ui.ds_vattu_tablewidget.setColumnCount(3)
                for row_index, row in enumerate(result):
                    for col_index,value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.main_ui.ds_vattu_tablewidget.setItem(row_index,col_index, item)
            else:
                self.main_ui.ds_vattu_tablewidget.clearContents()
                self.main_ui.ds_vattu_tablewidget.setItem(0,1,QtWidgets.QTableWidgetItem("Không có kết quả"))
    
    #Show data vật tư
    def show_data_vattu(self):
        query = """SELECT * FROM VatTu"""
        result = self._mysql_connector.execute_query(query,select=True)
        if result:
            self.main_ui.ds_vattu_tablewidget.setRowCount(len(result))
            self.main_ui.ds_vattu_tablewidget.setColumnCount(3)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.main_ui.ds_vattu_tablewidget.setItem(row_index,col_index,item)
        else:
            print("Không có data vật tư")
    
    #CRUD Vật tư
    def get_ma(self):
        query = "SELECT ma_vt FROM VatTu ORDER BY ma_vt DESC LIMIT 1"
        obj_type = "VT"
        byte = 3
        first_id = "001"
        ma_vt = self.main_form.generate_ma(query=query,obj_type=obj_type,byte=byte,first_id=first_id)
        return ma_vt
    #Insert vật tư
    def insert_vt(self):
        try:
            ma_vt = self.get_ma()
            ten_vt = self.inventory_ui.ten_vt_edit.text()
            sl_vt = self.inventory_ui.sl_vt_edit.text()
            
            query = "INSERT INTO VatTu (ma_vt,ten_vt,so_luong_vt) VALUES (%s,%s,%s)"
            params = (ma_vt,ten_vt,sl_vt)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_vattu()
            self.inventory_ui.ten_vt_edit.clear()
            self.inventory_ui.sl_vt_edit.clear()
            print("Insert successfully")
            self.inventory_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
    
    def get_info_vt(self):
        try:
            selected_items = self.main_ui.ds_vattu_tablewidget.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_vattu_tablewidget.currentRow()
            ma_vt = self.main_ui.ds_vattu_tablewidget.item(row,0).text()
            ten_vt = self.main_ui.ds_vattu_tablewidget.item(row,1).text()
            sl_vt = self.main_ui.ds_vattu_tablewidget.item(row,2).text()
            self.inventory_edit_ui.ma_vt_edit.setText(ma_vt)
            self.inventory_edit_ui.ten_vt_edit.setText(ten_vt)
            self.inventory_edit_ui.sl_vt_edit.setText(sl_vt)
            return ma_vt
        except mysql.connector.Error as err:
                print(f"Lỗi: {err}")   
    
    def update_vt(self):
        try:
            ma_vt = self.inventory_edit_ui.ma_vt_edit.text()
            ten_vt = self.inventory_edit_ui.ten_vt_edit.text()
            sl_vt = self.inventory_edit_ui.sl_vt_edit.text()
            
            query = "UPDATE VatTu SET ten_vt=%s,so_luong_vt=%s WHERE ma_vt=%s"
            params = (ten_vt,sl_vt,ma_vt)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_vattu()
            print('Update successfully')
            self.inventory_edit_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")    
    
    def delete_vt(self):
        try:
            ma_vt = self.get_info_vt()
            query = "DELETE FROM VatTu WHERE ma_vt=%s"
            params = (ma_vt,)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá vtách hàng {ma_vt} Không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self._mysql_connector.execute_query(query=query,params=params)
                self.show_data_vattu()
                print("Delete successfully")
            else:
                return
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
            
            
        
        