import sys


from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        #Configurando o layout basico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        
        #Titulo da janela
        self.setWindowTitle('Coloque o titulo')
        
        
    def adjustFixedSize(self):
        #Ultima coisa a ser executada
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
    
    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        # self.adjustFixedSize()

    def makeMsgBox(self):
        return QMessageBox(self)