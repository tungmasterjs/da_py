create database 4MEN_BARBERSHOP;
use 4MEN_BARBERSHOP;
create table Tho(
	ma_tho varchar(5) primary key,
    ten_tho varchar(50),
    sdt_tho bigint(10),
    so_nam_kinh_nghiem int
);
create table KhachHang(
	ma_kh varchar(7) primary key,
	ten_kh varchar(50),
    sdt_kh bigint(10),
    so_lan_den int,
    loai_kh enum('Thường','VIP')
);
create table DichVu(
	ma_dv varchar(5) primary key,
    ten_dv varchar(100),
    don_gia float
);
create table DatLich(
	ma_dl varchar(10) primary key,
    ma_kh varchar(7),
    ma_tho varchar(5),
    ma_dv varchar(5),
    thoi_gian_dat datetime
);
create table VatTu(
	ma_vt varchar(5) primary key,
    ten_vt varchar(50),
    so_luong_vt int
);
create table HoaDon(
	so_hd varchar(10) primary key,
    ma_kh varchar(7),
    ma_tho varchar(5),
    tong_tien decimal(10,2),
    thoi_gian_tt datetime
);
create table ChiTietHoaDon(
	so_cthd varchar(10) primary key,
    so_hd varchar(10),
    ma_dv varchar(5),
    so_luong_dv int,
    don_gia float,
    thanh_tien float
);
create table user_acc(
	user_id varchar(50) primary key,
    user_name varchar(50),
    pass_word varchar(16),
    user_role enum('Admin','User')
);

ALTER TABLE DatLich
ADD CONSTRAINT fk_datlich_khachhang FOREIGN KEY (ma_kh) REFERENCES KhachHang(ma_kh),
ADD CONSTRAINT fk_datlich_tho FOREIGN KEY (ma_tho) REFERENCES Tho(ma_tho),
ADD CONSTRAINT fk_datlich_dichvu FOREIGN KEY (ma_dv) REFERENCES DichVu(ma_dv);
ALTER TABLE HoaDon
ADD CONSTRAINT fk_hoadon_khachhang FOREIGN KEY (ma_kh) REFERENCES KhachHang(ma_kh),
ADD CONSTRAINT fk_hoadon_tho FOREIGN KEY (ma_tho) REFERENCES Tho(ma_tho);
ALTER TABLE ChiTietHoaDon
ADD CONSTRAINT fk_chitiethoadon_hoadon FOREIGN KEY (so_hd) REFERENCES HoaDon(so_hd),
ADD CONSTRAINT fk_chitiethoadon_dichvu FOREIGN KEY (ma_dv) REFERENCES DichVu(ma_dv);

INSERT INTO tho (ma_tho, ten_tho, sdt_tho, so_nam_kinh_nghiem)
VALUES
('TH001', 'Nguyễn Văn Anh', '0123456789', 5),
('TH002', 'Trần Văn Bình', '0123456780', 3),
('TH003', 'Lê Văn Đức', '0123456701', 8),
('TH004', 'Phạm Văn Đông', '0123456702', 2),
('TH005', 'Hoàng Văn Hải', '0123456703', 6),
('TH006', 'Vũ Văn Hiếu', '0123456704', 4),
('TH007', 'Nguyễn Văn Hùng', '0123456705', 9),
('TH008', 'Trần Văn Lâm', '0123456706', 1),
('TH009', 'Lê Văn Long', '0123456707', 7),
('TH010', 'Phạm Văn Minh', '0123456708', 10);

INSERT INTO KhachHang (ma_kh, ten_kh, sdt_kh, so_lan_den, loai_kh)
VALUES
('KH00001','Nguyễn Văn A', '0123456001', 5, 'Thường'),
('KH00002','Trần Văn B', '0123456002', 3, 'Thường'),
('KH00003','Lê Văn C', '0123456003', 8, 'Thường'),
('KH00004','Phạm Văn D', '0123456004', 2, 'Thường'),
('KH00005','Hoàng Văn E', '0123456005', 6, 'Thường'),
('KH00006','Vũ Văn F', '0123456006', 4, 'Thường'),
('KH00007','Nguyễn Văn G', '0123456007', 9, 'Thường'),
('KH00008','Trần Văn H', '0123456008', 1, 'Thường'),
('KH00009','Lê Văn I', '0123456009', 7, 'Thường'),
('KH00010','Phạm Văn J', '0123456010', 10, 'VIP'),
('KH00011','Hoàng Văn K', '0123456011', 5, 'Thường'),
('KH00012','Vũ Văn L', '0123456012', 3, 'Thường'),
('KH00013','Nguyễn Văn M', '0123456013', 8, 'Thường'),
('KH00014','Trần Văn N', '0123456014', 2, 'Thường'),
('KH00015','Lê Văn O', '0123456015', 6, 'Thường'),
('KH00016','Phạm Văn P', '0123456016', 4, 'Thường'),
('KH00017','Hoàng Văn Q', '0123456017', 9, 'VIP'),
('KH00018','Vũ Văn R', '0123456018', 1, 'Thường'),
('KH00019','Nguyễn Văn S', '0123456019', 7, 'Thường'),
('KH00020','Trần Văn T', '0123456020', 10, 'VIP'),
('KH00021','Nguyễn Văn U', '0123456021', 15, 'VIP'),
('KH00022','Trần Văn V', '0123456022', 12, 'VIP'),
('KH00023','Lê Văn X', '0123456023', 11, 'VIP'),
('KH00024','Phạm Văn Y', '0123456024', 14, 'VIP'),
('KH00025','Hoàng Văn Z', '0123456025', 20, 'VIP'),
('KH00026','Vũ Văn W', '0123456026', 18, 'VIP'),
('KH00027','Nguyễn Thanh', '0123456027', 13, 'VIP'),
('KH00028','Trần Thịnh', '0123456028', 16, 'VIP');



INSERT INTO DichVu (ma_dv, ten_dv, don_gia)
VALUES
('DV001', 'Cắt tóc cơ bản', 100000),
('DV002', 'Cắt tóc phong cách', 150000),
('DV003', 'Cạo râu cơ bản', 50000),
('DV004', 'Cạo râu phong cách', 80000),
('DV005', 'Gội đầu', 70000),
('DV006', 'Nhuộm tóc', 200000),
('DV007', 'Dưỡng tóc', 120000),
('DV008', 'Hấp dầu', 90000),
('DV009', 'Duỗi tóc', 250000),
('DV010', 'Cắt tóc trẻ em', 120000);

INSERT INTO VatTu (ma_vt, ten_vt, so_luong_vt)
VALUES
('VT001', 'Kéo', 10),
('VT002', 'Bàn chải', 15),
('VT003', 'Gương', 20),
('VT004', 'Bàn làm việc', 5),
('VT005', 'Ghế cắt tóc', 8),
('VT006', 'Kệ để đồ', 12),
('VT007', 'Bình xịt nước', 10),
('VT008', 'Bộ lau chùi', 10),
('VT009', 'Thuốc nhuộm', 20),
('VT010', 'Dụng cụ duỗi đồ', 10),
('VT011', 'Tông đơ cắt tóc', 15),
('VT012', 'Tông đơ cạo râu', 15),
('VT013', 'Tông đơ cắt viền', 10);

INSERT INTO user_acc (user_id, user_name, pass_word, user_role)
VALUES
('admin','Admin','admin','Admin');

INSERT INTO HoaDon (so_hd, ma_kh, ma_tho, tong_tien, thoi_gian_tt)
VALUES
('HD001', 'KH00001', 'TH001', 150000, '2024-04-01 08:30:00'),
('HD002', 'KH00002', 'TH002', 250000, '2024-04-02 10:45:00'),
('HD003', 'KH00003', 'TH003', 200000, '2024-04-03 12:00:00'),
('HD004', 'KH00004', 'TH004', 100000, '2024-04-04 13:15:00'),
('HD005', 'KH00005', 'TH005', 300000, '2024-04-05 14:30:00'),
('HD006', 'KH00006', 'TH006', 180000, '2024-04-06 16:45:00'),
('HD007', 'KH00007', 'TH007', 220000, '2024-04-07 18:00:00'),
('HD008', 'KH00008', 'TH008', 260000, '2024-04-08 08:15:00'),
('HD009', 'KH00009', 'TH009', 320000, '2024-04-09 09:30:00'),
('HD010', 'KH00010', 'TH010', 280000, '2024-04-10 10:45:00');



INSERT INTO ChiTietHoaDon (so_cthd, so_hd, ma_dv, so_luong_dv, don_gia, thanh_tien)
VALUES
('CTHD001', 'HD001', 'DV001', 1, 100000, 100000),
('CTHD002', 'HD001', 'DV002', 1, 150000, 150000),
('CTHD003', 'HD002', 'DV003', 2, 50000, 100000),
('CTHD004', 'HD002', 'DV005', 1, 70000, 70000),
('CTHD005', 'HD003', 'DV001', 1, 100000, 100000),
('CTHD006', 'HD003', 'DV003', 1, 50000, 50000),
('CTHD007', 'HD004', 'DV002', 1, 150000, 150000),
('CTHD008', 'HD004', 'DV005', 1, 70000, 70000),
('CTHD009', 'HD005', 'DV001', 2, 100000, 200000),
('CTHD010', 'HD005', 'DV002', 1, 150000, 150000),
('CTHD011', 'HD006', 'DV001', 1, 100000, 100000),
('CTHD012', 'HD006', 'DV004', 1, 80000, 80000),
('CTHD013', 'HD007', 'DV002', 1, 150000, 150000),
('CTHD014', 'HD007', 'DV003', 1, 50000, 50000),
('CTHD015', 'HD008', 'DV001', 2, 100000, 200000),
('CTHD016', 'HD008', 'DV002', 1, 150000, 150000),
('CTHD017', 'HD009', 'DV001', 1, 100000, 100000),
('CTHD018', 'HD009', 'DV004', 1, 80000, 80000),
('CTHD019', 'HD010', 'DV002', 1, 150000, 150000),
('CTHD020', 'HD010', 'DV003', 1, 50000, 50000);

INSERT INTO DatLich (ma_dl, ma_kh, ma_tho, ma_dv, thoi_gian_dat)
VALUES
('DL001', 'KH00001', 'TH001', 'DV001', '2024-04-01 08:30:00'),
('DL002', 'KH00002', 'TH002', 'DV002', '2024-04-02 10:45:00'),
('DL003', 'KH00003', 'TH003', 'DV003', '2024-04-03 12:00:00'),
('DL004', 'KH00004', 'TH004', 'DV004', '2024-04-04 13:15:00'),
('DL005', 'KH00005', 'TH005', 'DV005', '2024-04-05 14:30:00'),
('DL006', 'KH00006', 'TH006', 'DV006', '2024-04-06 16:45:00'),
('DL007', 'KH00007', 'TH007', 'DV007', '2024-04-07 18:00:00'),
('DL008', 'KH00008', 'TH008', 'DV008', '2024-04-08 08:15:00'),
('DL009', 'KH00009', 'TH009', 'DV009', '2024-04-09 09:30:00'),
('DL010', 'KH00010', 'TH010', 'DV010', '2024-04-10 10:45:00');


