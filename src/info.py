from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from config.variables import SML_FONT_SIZE

class Info(QLabel):
    def __init_subclass__(self,  parent, *args, **kwargs):
        return super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SML_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)