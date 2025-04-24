import sys
sys.path.append('../DO AN')
from PyQt5 import QtWidgets,QtCore
from Fourmenbarbershop_package.gui import login_ui

class LoginForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        #Khai báo login form
        self.login_ui = login_ui.Ui_login_form()
        self.login_ui.setupUi(self)
        
        self.login_ui.login_btn.clicked.connect(self.handle_login)
        
    def handle_login(self):
        pass
        

    
            