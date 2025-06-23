from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from config.variables import MID_FONT_SIZE

from utils.utils import isEmpty, isNumOrDot, isValidNumber

#Circular Import
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.display import Display
    from info import Info

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MID_FONT_SIZE)
        font.setItalic(False)
        font.setBold(True)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        # self.setCheckable(True)
        # self.setProperty('cssClass', 'specialButton')

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation  = ''
        self._equationInitialValue = 'Sua Conta'
        self._left = None
        self._right = None
        self._op = None
        
        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
    
    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            # print(i, row)
            for j, button_text in enumerate(row):
                button = Button(button_text)
                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertButtonTextToDisplay,button)
                self._connectButtonCliked(button, slot)
    
    def _connectButtonCliked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            # slot = self._makeSlot(self.display.clear,button)
            self._connectButtonCliked(button, self._clear)
            # button.clicked.connect(self.display.clear)

        if text in '+-/*':
            self._connectButtonCliked(button, 
                self._makeSlot(self._operatorClicked, button))


    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot


    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
    
    def _operatorClicked(self, button):
        buttonText = button.text() # Operadores
        displayText = self.display.text() # left
        self.display.clear()

        if not isValidNumber(displayText) and self.left is None:
            print('Não tem nada para colocar no valor da esquerda')
            return
        if self._left is None:
            self._left = float(displayText)

        self.op = buttonText
        self.equation = f'{self._left} {self.op} ??'