from PySide6.QtWidgets import QLineEdit
from config.variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils.utils import isEmpty

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key()

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return] # KEYS.Key_Equal

        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete] # KEYS.Key_D

        isESC = key in [KEYS.Key_Escape] # KEUS.Key_C

        if isEnter or text == '=':
            print('Enter pressionado, sinal emitido', type(self).__name__)
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete or text.upper() == 'D':
            print('isDelete pressionado, sinal emitido', type(self).__name__)
            self.delPressed.emit()
            return event.ignore()
        
        if isESC or text.upper() == 'C':
            print('isESC pressionado, sinal emitido', type(self).__name__)
            self.clearPressed.emit()
            return event.ignore()
        
        # Não Passar daqui se não tiver texto
        if isEmpty(text):
            return event.ignore()
        print('Texto:', text)
