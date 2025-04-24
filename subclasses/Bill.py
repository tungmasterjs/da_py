import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import bill_ui
from Fourmenbarbershop_package.subclasses import Payment
from Fourmenbarbershop_package.subclasses import Statistics
from Fourmenbarbershop_package.gui import FourMenBarberShop_ui
from Fourmenbarbershop_package import FourMenBarberShop
import mysql.connector

class BillWidget():
    def __init__(self,mysql_connector,main_ui, main_form):
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        self.tong_tien = 0
        
        self.start_date = self.main_ui.start_date_edit.date()
        self.end_date = self.main_ui.end_date_edit.date()
        
        #Khai báo bill form
        self.bill_form = QtWidgets.QWidget()
        self.bill_ui = bill_ui.Ui_bill_form()
        self.bill_ui.setupUi(self.bill_form)
    
    
    def open_bill_form(self):
        self.bill_form.show()
        self.show_data_hd()
        
        #Gọi hàm tìm kiếm hoá đơn
        self.bill_ui.tim_hd_btn.clicked.connect(self.tim_hd)
        self.bill_ui.tim_hd_tbx.returnPressed.connect(self.bill_ui.tim_hd_btn.click)
        
        
        #Hiện gợi ý, lịch sử
        self.completer = QtWidgets.QCompleter(self.hien_goi_y())
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.bill_ui.tim_hd_tbx.setCompleter(self.completer)

        self.bill_ui.ds_hd_tb.itemSelectionChanged
        self.bill_ui.ds_hd_tb.cellDoubleClicked.connect(self.get_info_hd)
        
        self.bill_ui.dateEdit.dateChanged.connect(self.loc_hoa_don)
        
        self.bill_ui.xoa_hd_btn.clicked.connect(self.delete_hd)
        
    def hien_goi_y(self):
        query = "SELECT DISTINCT so_hd,ma_kh,sdt_kh,ma_tho FROM HoaDon"
        return self.main_form.get_search_history(query=query)

    #Tìm kiếm
    def tim_hd(self):
        if self.bill_ui.tim_hd_tbx.text() == '':
            self.show_data_hd()
        else:
            query = "SELECT * FROM HoaDon WHERE so_hd=%s OR ma_kh=%s OR sdt_kh=%s OR ma_tho=%s"
            params = (self.bill_ui.tim_hd_tbx.text(),self.bill_ui.tim_hd_tbx.text(),self.bill_ui.tim_hd_tbx.text(),self.bill_ui.tim_hd_tbx.text())
            result = self._mysql_connector.execute_query(query=query,params=params,select=True)
            if result:
                self.bill_ui.ds_hd_tb.setRowCount(len(result))
                self.bill_ui.ds_hd_tb.setColumnCount(7)
                for row_index, row in enumerate(result):
                    for col_index,value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.bill_ui.ds_hd_tb.setItem(row_index,col_index, item)
            else:
                self.bill_ui.ds_hd_tb.clearContents()
                self.bill_ui.ds_hd_tb.setItem(0,2,QtWidgets.QTableWidgetItem("Không có kết quả"))
    
    
    def loc_hoa_don(self):
        query = """SELECT DISTINCT*
                FROM HoaDon
                INNER JOIN KhachHang ON HoaDon.ma_kh = KhachHang.ma_kh
                INNER JOIN Tho ON HoaDon.ma_tho = Tho.ma_tho
                WHERE DATE_FORMAT(HoaDon.thoi_gian_tt, '%Y-%m-%d') = %s
                ORDER BY HoaDon.thoi_gian_tt DESC"""
        date = self.bill_ui.dateEdit.date()
        date_str = date.toString("yyyy-MM-dd")
        print(date_str)
        params = (date_str,)
        result = self._mysql_connector.execute_query(query, params=params, select=True)

        if result:
            self.bill_ui.ds_hd_tb.setRowCount(len(result))
            self.bill_ui.ds_hd_tb.setColumnCount(7)
            for row_index, row in enumerate(result):
                for col_index, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.bill_ui.ds_hd_tb.setItem(row_index, col_index, item)
        else:
            self.bill_ui.ds_hd_tb.clearContents()
            self.bill_ui.ds_hd_tb.setItem(0, 2, QtWidgets.QTableWidgetItem("Không có hoá đơn cho ngày này"))

    
    #Show data hoá đơn
    def show_data_hd(self):
        query = "SELECT * FROM HoaDon"
        result = self._mysql_connector.execute_query(query,select=True)
        if result:
            self.bill_ui.ds_hd_tb.setRowCount(len(result))
            self.bill_ui.ds_hd_tb.setColumnCount(7)
            for row_index,row in enumerate(result):
                for col_index,value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.bill_ui.ds_hd_tb.setItem(row_index,col_index,item)
        else:
            print("Không có data hoá đơn")
            
    
    def get_info_hd(self):
        self.bill_form.close()
        try:
            selected_items = self.bill_ui.ds_hd_tb.selectedItems()
            if not selected_items:
                return
            row = self.bill_ui.ds_hd_tb.currentRow()
            so_hd = self.bill_ui.ds_hd_tb.item(row,0).text()
            ma_kh = self.bill_ui.ds_hd_tb.item(row,1).text()
            sdt_kh = self.bill_ui.ds_hd_tb.item(row,2).text()
            ma_tho = self.bill_ui.ds_hd_tb.item(row,3).text()
            giam_gia = self.bill_ui.ds_hd_tb.item(row,4).text()
            tong_tien = self.bill_ui.ds_hd_tb.item(row,5).text()
            self.tong_tien = float(tong_tien)
            thoi_gian_tt = self.bill_ui.ds_hd_tb.item(row,6).text()
            
            #Get tên khách hàng khi nhập sdt
            query = "SELECT ten_kh FROM KhachHang WHERE ma_kh=%s"
            result = self._mysql_connector.execute_query(query=query,params=(ma_kh,),select=True)
            if result:
                ten_kh = result[0][0]
                self.main_ui.ten_kh_tbx.setText(ten_kh)
            else:
                ten_kh = 'Khách vãng lai'
                self.main_ui.ten_kh_tbx.setText(ten_kh)
            
            #Lấy tên thợ từ table
            query_tho = "SELECT ten_tho FROM Tho WHERE ma_tho = %s"
            result_tho = self._mysql_connector.execute_query(query=query_tho,params=(ma_tho,),select=True)
            if result_tho:
                ten_tho = result_tho[0][0]
            else:
                ten_tho = None
            
            self.main_ui.so_hd_tbx.setText(so_hd)
            self.main_ui.time_tbx.setText(thoi_gian_tt)
            self.main_ui.sdt_kh_tbx.setText(sdt_kh)
            self.main_ui.ten_kh_tbx.setText(ten_kh)
            self.main_ui.giam_gia_tbx.setText(giam_gia)
            self.main_ui.tong_tien_tbx.setText(str(self.tong_tien))
                
            query_dv = "SELECT ma_dv,so_luong_dv,don_gia,thanh_tien FROM ChiTietHoaDon WHERE so_hd=%s"
            result_dv = self._mysql_connector.execute_query(query=query_dv,params=(so_hd,),select=True)
            
            self.main_ui.ds_dich_vu_tb.setRowCount(0)
            
            for record in result_dv:
                ma_dv, so_luong, don_gia, thanh_tien = record
                formatted_dg = "{:,.0f}".format(don_gia).replace(',','.')
                formatted_tt = "{:,.0f}".format(thanh_tien).replace(',','.')
                # Lấy tên dịch vụ từ ma_dv
                query_dv_name = "SELECT ten_dv FROM DichVu WHERE ma_dv = %s"
                result_dv_name = self._mysql_connector.execute_query(query=query_dv_name, params=(ma_dv,), select=True)
                if result_dv_name:
                    ten_dv = result_dv_name[0][0]
                else:
                    ten_dv = None

                row_count = self.main_ui.ds_dich_vu_tb.rowCount()
                self.main_ui.ds_dich_vu_tb.insertRow(row_count)
                self.main_ui.ds_dich_vu_tb.setItem(row_count,0,self.main_form.create_centered_item(ten_dv))
                self.main_ui.ds_dich_vu_tb.setItem(row_count,1,self.main_form.create_centered_item(str(so_luong)))
                self.main_ui.ds_dich_vu_tb.setItem(row_count,2,self.main_form.create_centered_item(str(formatted_dg)))
                self.main_ui.ds_dich_vu_tb.setItem(row_count,3,self.main_form.create_centered_item(str(formatted_tt)))
                                                   
            #Set số lượng về 1
            self.main_ui.sl_dich_vu_cbx.setValue(1)
            #Set combobox về giá trị đầu
            self.main_ui.ten_tho_cbx.setCurrentText(str(ten_tho))
            self.main_ui.dich_vu_cbx.setCurrentIndex(0)
            
            Payment.PaymentWidget.tinh_tien(self)
            
        except mysql.connector.Error as err:
            print(f'Lỗi: {err}')
            
    
    #Xoá - Hoá đơn
    def delete_hd(self):
        try:
            row = self.bill_ui.ds_hd_tb.currentRow()
            so_hd = self.bill_ui.ds_hd_tb.item(row,0).text()
            
            query_cthd = "DELETE FROM ChiTietHoaDon WHERE so_hd = %s"
            params = (so_hd,)
            
            
            query_hd = "DELETE FROM HoaDon WHERE so_hd = %s"
            
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setWindowTitle("Xác nhận xoá")
            self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
            self.msgBox.setText(f"Có chắc bạn muốn xoá hoá đơn {so_hd} không?")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = self.msgBox.exec()
            if ret == self.msgBox.Yes:
                self._mysql_connector.execute_query(query=query_cthd,params=params)
                self._mysql_connector.execute_query(query=query_hd,params=params)
                self.show_data_hd()
                Statistics.StatisticsWidget.cap_nhat_dt_slhd(self)
                print("Delete successfully")
            else:
                return
        except mysql.connector.Error as err:
            print(f"Lỗi: {err}")
