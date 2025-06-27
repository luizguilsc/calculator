from PySide6.QtWidgets import QLineEdit
from config.variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils.utils import isEmpty, isNumOrDot

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

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

        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P] # Operadores

        if isEnter or text == '=':
            # print('Enter pressionado, sinal emitido', type(self).__name__)
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete or text.upper() == 'D':
            # print('isDelete pressionado, sinal emitido', type(self).__name__)
            self.delPressed.emit()
            return event.ignore()
        
        if isESC or text.upper() == 'C':
            # print('isESC pressionado, sinal emitido', type(self).__name__)
            self.clearPressed.emit()
            return event.ignore()
        
        if isOperator:
            # print('isOperator pressionado, sinal emitido', type(self).__name__)
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
        
        # Não Passar daqui se não tiver texto
        if isEmpty(text):
            return event.ignore()
        # print('Texto:', text)

        if isNumOrDot(text):
            # print('inputPressed pressionado, sinal emitido', type(self).__name__)
            self.inputPressed.emit(text)
            return event.ignore()
