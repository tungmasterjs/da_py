import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import booking_ui
from Fourmenbarbershop_package.gui import booking_edit
from Fourmenbarbershop_package.gui import FourMenBarberShop_ui
import mysql.connector
import datetime

class BookingWidget:
    def __init__(self, mysql_connector, main_ui, main_form):
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        
        #Khai báo customer form - Mở form thêm lịch hẹn
        self.booking_form = QtWidgets.QDialog()
        self.booking_ui = booking_ui.Ui_booking_form()
        self.booking_ui.setupUi(self.booking_form)
        
        #Khai báo customer_edit form
        self.booking_edit_form = QtWidgets.QDialog()
        self.booking_edit_ui = booking_edit.Ui_booking_edit_form()
        self.booking_edit_ui.setupUi(self.booking_edit_form)
        self.main_ui.ds_lich_hen_tb.itemSelectionChanged.connect(self.get_info_dl)
        
        self.main_ui.calendarWidget.selectionChanged.connect(self.loc_lich)
        
    def open_booking_form(self):
        self.booking_form.show()
        self.booking_ui.ma_lich_edit.setText(str(self.get_ma()))
        self.booking_ui.ma_tho_chkbx.addItems(self.get_ten_tho())
        self.booking_ui.dich_vu_lich_chkbx.addItems(self.get_dich_vu())
        self.booking_ui.luu_lich_btn.clicked.connect(self.insert_dl)
        self.booking_ui.sdt_kh_lich_edit.textChanged.connect(self.get_ten_kh)
        self.booking_ui.ket_thuc_lich_btn.clicked.connect(self.close_booking_form)
    def close_booking_form(self):
        self.booking_form.close()
        
    def open_booking_edit_form(self):
        self.booking_edit_form.show()
        self.booking_edit_ui.ma_tho_chkbx.addItems(self.get_ten_tho())
        self.booking_edit_ui.dich_vu_lich_chkbx.addItems(self.get_dich_vu())
        self.booking_edit_ui.sdt_kh_lich_edit.textChanged.connect(self.get_ten_kh)
        self.booking_edit_ui.luu_lich_btn.clicked.connect(self.update_dl)
        self.booking_edit_ui.ket_thuc_lich_btn.clicked.connect(self.close_booking_edit_form)
    def close_booking_edit_form(self):
        self.booking_edit_form.close()
    

    #Show data lịch hẹn
    def show_data_lichhen(self):
        try:
            query = """SELECT DatLich.ma_dl,DatLich.ten_kh,DatLich.sdt_kh,Tho.ten_tho,DichVu.ten_dv,DatLich.thoi_gian_dat FROM DatLich 
                        INNER JOIN Tho ON DatLich.ma_tho=Tho.ma_tho
                        INNER JOIN DichVu ON DatLich.ma_dv=DichVu.ma_dv
                        ORDER BY thoi_gian_dat DESC"""

            result = self._mysql_connector.execute_query(query,select=True)
            
            if result:
                self.main_ui.ds_lich_hen_tb.setRowCount(len(result))
                self.main_ui.ds_lich_hen_tb.setColumnCount(6)
                for row_index,row in enumerate(result):
                    for col_index,value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.main_ui.ds_lich_hen_tb.setItem(row_index,col_index,item)
            else:
                print("Không có data đặt lịch")
        except mysql.connector.Error as err:
            print(err)

    #Hàm tìm tên khách hàng khi nhập sdt
    def get_ten_kh(self):
        sdt_kh = self.booking_ui.sdt_kh_lich_edit.text()
        query = "SELECT ten_kh FROM KhachHang WHERE sdt_kh=%s"
        result = self._mysql_connector.execute_query(query=query,params=(sdt_kh,),select=True)
        if result:
            ten_kh = result[0][0]
            self.booking_ui.ten_kh_lich_edit.setText(ten_kh)
        else:
            ten_kh = ''
            self.booking_ui.ten_kh_lich_edit.setText(ten_kh)
    
    #Lấy ngày đang chọn
    def get_ngay(self):
        date = self.main_ui.calendarWidget.selectedDate()
        date_str = QtCore.QDate.toString(date,"yyyy-MM-dd")
        return date_str
    
    #Lọc lịch theo ngày đã chọn
    def loc_lich(self):
        query = """SELECT DatLich.ma_dl,DatLich.ten_kh,DatLich.sdt_kh,Tho.ten_tho,DichVu.ten_dv,DatLich.thoi_gian_dat FROM DatLich 
                    INNER JOIN Tho ON DatLich.ma_tho=Tho.ma_tho
                    INNER JOIN DichVu ON DatLich.ma_dv=DichVu.ma_dv
                    WHERE DATE_FORMAT(DatLich.thoi_gian_dat, '%Y-%m-%d') = %s
                    ORDER BY thoi_gian_dat DESC"""
        date = self.get_ngay()
        params = (date,)
        result = self._mysql_connector.execute_query(query,params=params,select=True)
        
        if result:
            self.main_ui.ds_lich_hen_tb.setRowCount(len(result))
            self.main_ui.ds_lich_hen_tb.setColumnCount(6)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.main_ui.ds_lich_hen_tb.setItem(row_index,col_index,item)
        else:
            self.main_ui.ds_lich_hen_tb.clearContents()
            self.main_ui.ds_lich_hen_tb.setItem(0,2,QtWidgets.QTableWidgetItem("Không có lịch cho ngày này"))
        
              
    def get_ten_tho(self):
        query = "SELECT ten_tho FROM Tho"
        result = self._mysql_connector.execute_query(query=query,select=True)
        l_ten_tho = [result[0] for result in result]
        return l_ten_tho
    
    def get_dich_vu(self):
        query = "SELECT ten_dv FROM DichVu"
        result = self._mysql_connector.execute_query(query=query,select=True)
        l_ten_dv = [result[0] for result in result]
        return l_ten_dv

    def get_ma(self):
        query = "SELECT ma_dl FROM DatLich ORDER BY ma_dl DESC LIMIT 1"
        obj_type = "DL"
        byte = 3
        first_id = "001"
        ma_dl = self.main_form.generate_ma(query=query,obj_type=obj_type,byte=byte,first_id=first_id)
        return ma_dl
    
    #Insert - Lịch
    def insert_dl(self):
        try:
            ma_dl = self.get_ma()
            self.booking_ui.ma_lich_edit.setText(ma_dl)
            sdt_kh = self.booking_ui.sdt_kh_lich_edit.text()
            ten_kh = self.booking_ui.ten_kh_lich_edit.text()
            thoi_gian_dat = self.booking_ui.time_lich_chkbx.dateTime()
            thoi_gian_dat_str = thoi_gian_dat.toString("yyyy-MM-dd HH:mm:ss")
            
            #Lấy mã thợ từ combobox
            ten_tho = self.booking_ui.ma_tho_chkbx.currentText()
            query_tho = "SELECT ma_tho FROM Tho WHERE ten_tho = %s"
            result_tho = self._mysql_connector.execute_query(query=query_tho,params=(ten_tho,),select=True)
            if result_tho:
                ma_tho = result_tho[0][0]
            else:
                ma_tho = None
            
            #Lấy mã dịch vụ từ combobox
            ten_dv = self.booking_ui.dich_vu_lich_chkbx.currentText()
            query_dv = "SELECT ma_dv FROM DichVu WHERE ten_dv = %s"
            result_dv = self._mysql_connector.execute_query(query=query_dv,params=(ten_dv,),select=True)
            if result_dv:
                ma_dv = result_dv[0][0]
            else:
                ma_dv = None
            
                        
            query = "INSERT INTO DatLich (ma_dl,sdt_kh,ten_kh,ma_tho,ma_dv,thoi_gian_dat) VALUES (%s,%s,%s,%s,%s,%s)"
            params = (ma_dl,sdt_kh,ten_kh,ma_tho,ma_dv,thoi_gian_dat_str)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_lichhen()
            self.booking_ui.sdt_kh_lich_edit.clear()
            self.booking_ui.ten_kh_lich_edit.clear()               
            self.booking_ui.ma_tho_chkbx.clear()
            self.booking_ui.dich_vu_lich_chkbx.clear()
            #self.booking_ui.
            self.booking_form.close()
            print("Insert successfully")
        except mysql.connector.Error as err:
            print(f'Lỗi: {err}')
    
    def get_info_dl(self):
        try:
            selected_items = self.main_ui.ds_lich_hen_tb.selectedItems()
            if not selected_items:
                return
            row = self.main_ui.ds_lich_hen_tb.currentRow()
            ma_dl = self.main_ui.ds_lich_hen_tb.item(row,0).text()
            ten_kh = self.main_ui.ds_lich_hen_tb.item(row,1).text()
            sdt_kh = self.main_ui.ds_lich_hen_tb.item(row,2).text()
            ten_tho = self.main_ui.ds_lich_hen_tb.item(row,3).text()
            ten_dv = self.main_ui.ds_lich_hen_tb.item(row,4).text()
            thoi_gian_dat_str = self.main_ui.ds_lich_hen_tb.item(row,5).text()
            
            #Chuyển đổi chuỗi thời gian thành QDateTime
            thoi_gian_dat = QtCore.QDateTime.fromString(thoi_gian_dat_str, "yyyy-MM-dd HH:mm:ss")
            
            self.booking_edit_ui.ma_lich_edit.setText(ma_dl)
            self.booking_edit_ui.ten_kh_lich_edit.setText(ten_kh)
            self.booking_edit_ui.sdt_kh_lich_edit.setText(sdt_kh)
            self.booking_edit_ui.ma_tho_chkbx.setCurrentText(ten_tho)
            self.booking_edit_ui.dich_vu_lich_chkbx.setCurrentText(ten_dv)
            self.booking_edit_ui.time_lich_chkbx.setDateTime(thoi_gian_dat)
            return ma_dl
        except mysql.connector.Error as err:
            print(f'Lỗi: {err}')
            
    #Update - Thợ
    def update_dl(self):
        try:
            ma_dl = self.booking_edit_ui.ma_lich_edit.text()
            sdt_kh = self.booking_edit_ui.sdt_kh_lich_edit.text()
            ten_kh = self.booking_edit_ui.ten_kh_lich_edit.text()
            thoi_gian_dat = self.booking_edit_ui.time_lich_chkbx.dateTime()
            thoi_gian_dat_str = thoi_gian_dat.toString("yyyy-MM-dd HH:mm:ss")
     
            #Lấy mã thợ từ combobox
            ten_tho = self.booking_edit_ui.ma_tho_chkbx.currentText()
            query_tho = "SELECT ma_tho FROM Tho WHERE ten_tho = %s"
            result_tho = self._mysql_connector.execute_query(query=query_tho,params=(ten_tho,),select=True)
            if result_tho:
                ma_tho = result_tho[0][0]
            else:
                ma_tho = None
            
            #Lấy mã dịch vụ từ combobox
            ten_dv = self.booking_edit_ui.dich_vu_lich_chkbx.currentText()
            query_dv = "SELECT ma_dv FROM DichVu WHERE ten_dv = %s"
            result_dv = self._mysql_connector.execute_query(query=query_dv,params=(ten_dv,),select=True)
            if result_dv:
                ma_dv = result_dv[0][0]
            else:
                ma_dv = None
            
            query = "UPDATE DatLich SET sdt_kh=%s, ten_kh=%s, ma_tho=%s, ma_dv=%s, thoi_gian_dat=%s WHERE ma_dl=%s"
            params = (sdt_kh,ten_kh,ma_tho,ma_dv,thoi_gian_dat_str,ma_dl)
            self._mysql_connector.execute_query(query=query,params=params)
            self.show_data_lichhen()
            print('Update successfully')
            self.booking_edit_form.close()
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")

    #Xoá - Đặt lịch
    def delete_dl(self):
        try:
            ma_dl = self.get_info_dl()
            
            query = "DELETE FROM DatLich WHERE ma_dl = %s"
            params = (ma_dl,)
            self._mysql_connector.execute_query(query=query,params=params)
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá lịch hẹn {ma_dl} không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self._mysql_connector.execute_query(query,params=params)
                self.show_data_lichhen()
                print("Delete successfully")
            else:
                return
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
 