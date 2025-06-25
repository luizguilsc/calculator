import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.info import Info
from src.main_window import MainWindow
from src.buttons import Button, ButtonsGrid
from config.variables import WINDOW_ICON_PATH
from widgets.style import setupTheme
from widgets.display import Display


# def temp_label(texto):
#     label1 = QLabel(texto)
#     label1.setStyleSheet('font-size: 150px;')
#     return label1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    #Define um icone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    # Código para fazer o windows reconhecer o icone na taskbar
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    # Info
    info = Info()
    info.setText('Sua conta')
    info.configStyle()
    window.addWidgetToVLayout(info)
    
    # Display
    display = Display()
    display.setPlaceholderText("Digite Algo")
    window.addWidgetToVLayout(display)
    display.configStyle()

    #Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()