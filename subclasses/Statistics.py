import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets, QtCore
import mysql.connector
import datetime
from PyQt5.QtCore import QTimer, QDate
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StatisticsWidget:
    def __init__(self, mysql_connector, main_ui, main_form):
        super().__init__()
        self._mysql_connector = mysql_connector
        self.main_ui = main_ui
        self.main_form = main_form
        self.tong_tien = 0
        self.ds_dv = []
        self.so_hd = None
        self.time = None
        
        self.start_date = self.main_ui.start_date_edit.date()
        self.end_date = self.main_ui.end_date_edit.date()
        
        self.chart_dt()
        self.top_kh()
        self.top_tho()
        self.main_ui.start_date_edit.setDate(self.cap_nhat_dt_slhd_today())
        self.main_ui.end_date_edit.setDate(self.cap_nhat_dt_slhd_today())
        self.cap_nhat_dt_slhd()
        self.main_ui.start_date_edit.dateChanged.connect(self.update_date)
        self.main_ui.end_date_edit.dateChanged.connect(self.update_date)
        
    def update_date(self):
        self.start_date = self.main_ui.start_date_edit.date()
        self.end_date = self.main_ui.end_date_edit.date()
        self.cap_nhat_dt_slhd()
        self.top_kh()
        self.top_tho()
        
    def chart_dt(self):
        nam = self.main_ui.nam_chart.value()
        query = """SELECT MONTH(thoi_gian_tt), SUM(tong_tien) FROM HoaDon 
                WHERE YEAR(thoi_gian_tt) = %s 
                GROUP BY MONTH(thoi_gian_tt)
                ORDER BY SUM(tong_tien) DESC"""
        result = self._mysql_connector.execute_query(query, params=(nam,), select=True)
        
        if result:
            thang = np.array([row[0] for row in result])
            doanh_thu_thang = np.array([row[1] for row in result]) / 1_000_000
        
            fig, ax = plt.subplots()
            bars = plt.bar(thang, doanh_thu_thang, color='#880000', width=0.4)
            plt.xlabel("Tháng")
            plt.ylabel("Doanh thu (triệu đồng)")
            plt.title("Biểu đồ doanh thu theo tháng")
            ax.set_xticks(np.arange(1, 13))  # Từ tháng 1 đến 12
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0, 
                    height, 
                    f'{height:.2f}', 
                    ha='center', 
                    va='bottom'
                )
            # Tạo FigureCanvas từ biểu đồ
            canvas = FigureCanvas(fig)
            
            # Đặt FigureCanvas vào chart_widget
            layout = QtWidgets.QVBoxLayout(self.main_ui.chart_widget)
            layout.addWidget(canvas)
            
            # Cập nhật hiển thị
            canvas.draw()
        else:
            print("ko")
        
    def cap_nhat_dt_slhd_today(self):
        # Lấy ngày hôm nay
        ngay_hien_tai = QDate.currentDate()
        return ngay_hien_tai
    
    def cap_nhat_dt_slhd(self):
        try:
            if self.start_date > self.end_date:
                QtWidgets.QMessageBox.information(self.main_form, "Lỗi", "Ngày bắt đầu không được lớn hơn ngày kết thúc")
        except: 
            QtWidgets.QMessageBox.information(self.main_form, "Lỗi", "Ngày bắt đầu không được lớn hơn ngày kết thúc")
        
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        query_dt = """SELECT SUM(tong_tien) FROM HoaDon
                WHERE DATE(thoi_gian_tt) BETWEEN %s AND %s"""
            
        query_luot = """SELECT COUNT(*) FROM HoaDon
                WHERE DATE(thoi_gian_tt) BETWEEN %s AND %s"""
        params = (start_date_str, end_date_str)
        result_dt = self._mysql_connector.execute_query(query=query_dt, params=params, select=True)
        result_luot = self._mysql_connector.execute_query(query=query_luot, params=params, select=True)
        
        if result_dt and result_dt[0][0] is not None:
            doanh_thu = result_dt[0][0]
        else:
            doanh_thu = 0
        formatted_dt = "{:,.0f} đ".format(doanh_thu).replace(',', '.')
        self.main_ui.doanh_thu_label.setText(formatted_dt)
        
        if result_luot and result_luot[0][0] is not None:
            luot = result_luot[0][0]
        else:
            luot = 0
        formatted_luot = f"{luot} lượt"
        self.main_ui.so_luot_label.setText(formatted_luot)
        
    def top_kh(self):
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        query = """SELECT KhachHang.ten_kh, COUNT(*) AS so_lan FROM HoaDon
                    INNER JOIN KhachHang ON KhachHang.ma_kh = HoaDon.ma_kh
                    WHERE DATE(thoi_gian_tt) BETWEEN %s AND %s
                    GROUP BY KhachHang.ten_kh
                    ORDER BY so_lan DESC LIMIT 3"""

        params = (start_date_str, end_date_str)
        result = self._mysql_connector.execute_query(query=query, params=params, select=True)
        
        if result:
            try:
                self.main_ui.kh_top1.setText(result[0][0])
                self.main_ui.luot_kh1.setText(str(result[0][1]))
            except IndexError:
                self.main_ui.kh_top1.setText("Không có")
                self.main_ui.luot_kh1.setText("0")

            try:
                self.main_ui.kh_top2.setText(result[1][0])
                self.main_ui.luot_kh2.setText(str(result[1][1]))
            except IndexError:
                self.main_ui.kh_top2.setText("Không có")
                self.main_ui.luot_kh2.setText("0")

            try:
                self.main_ui.kh_top3.setText(result[2][0])
                self.main_ui.luot_kh3.setText(str(result[2][1]))
            except IndexError:
                self.main_ui.kh_top3.setText("Không có")
                self.main_ui.luot_kh3.setText("0")
        else:
            self.main_ui.kh_top1.setText("Không có")
            self.main_ui.luot_kh1.setText("0")
            self.main_ui.kh_top2.setText("Không có")
            self.main_ui.luot_kh2.setText("0")
            self.main_ui.kh_top3.setText("Không có")
            self.main_ui.luot_kh3.setText("0")

            
    def top_tho(self):
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        query = """SELECT Tho.ten_tho, COUNT(*) AS so_lan_hot FROM HoaDon
                INNER JOIN Tho ON Tho.ma_tho = HoaDon.ma_tho
                WHERE DATE(thoi_gian_tt) BETWEEN %s AND %s
                GROUP BY Tho.ten_tho
                ORDER BY so_lan_hot DESC LIMIT 3"""

        params = (start_date_str, end_date_str)
        result = self._mysql_connector.execute_query(query=query, params=params, select=True)
        
        if result:
            try:
                self.main_ui.tho_top1.setText(result[0][0])
                self.main_ui.lan_tho1.setText(str(result[0][1]))
            except IndexError:
                self.main_ui.tho_top1.setText("Không có")
                self.main_ui.lan_tho1.setText("0")

            try:
                self.main_ui.tho_top2.setText(result[1][0])
                self.main_ui.lan_tho2.setText(str(result[1][1]))
            except IndexError:
                self.main_ui.tho_top2.setText("Không có")
                self.main_ui.lan_tho2.setText("0")

            try:
                self.main_ui.tho_top3.setText(result[2][0])
                self.main_ui.lan_tho3.setText(str(result[2][1]))
            except IndexError:
                self.main_ui.tho_top3.setText("Không có")
                self.main_ui.lan_tho3.setText("0")
        else:
            self.main_ui.tho_top1.setText("Không có")
            self.main_ui.lan_tho1.setText("0")
            self.main_ui.tho_top2.setText("Không có")
            self.main_ui.lan_tho2.setText("0")
            self.main_ui.tho_top3.setText("Không có")
            self.main_ui.lan_tho3.setText("0")
