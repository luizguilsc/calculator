import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from config.variables import MID_FONT_SIZE

from utils.utils import isEmpty, isNumOrDot, isValidNumber, converToNumber

#Circular Import
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.display import Display
    from main_window import MainWindow
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
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',*args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
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
    
    def vouApagarVoce(self, *args):
        print(f'Signal pressionado, sinal recebido por "vouApagarVoce" em: ', type(self).__name__, args)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            # print(i, row)
            for j, button_text in enumerate(row):
                button = Button(button_text)
                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertToDisplay,button_text)
                self._connectButtonCliked(button, slot)
    
    def _connectButtonCliked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            # slot = self._makeSlot(self.display.clear,button)
            self._connectButtonCliked(button, self._clear)
            # button.clicked.connect(self.display.clear)
        
        if text == '◀':
            self._connectButtonCliked(button, self.display.backspace)
        
        if text == 'N':
            self._connectButtonCliked(button, self._invertNumber)

        if text in '+-/*^':
            self._connectButtonCliked(button, 
                self._makeSlot(self._configLeftOp, text))

        if text == '=':
            self._connectButtonCliked(button, self._eq)


    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = converToNumber(displayText) * -1

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()



    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
    
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text() # left
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Voce não digitou nada')
            return
        if self._left is None:
            self._left = converToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} {self._right}'
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta imcompleta')
            return
        
        self._right = converToNumber(displayText)
        self.equation = f'{self._left}{self._op}{self._right}'
        # if self._right is None:
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = converToNumber(str(result))
            
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisao por zero')

        except OverflowError:
            self._showError('Essa conta nao pode ser realizada')
        
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None


    def _makeDialog(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setInformativeText('''Texto absurdamente enorme''')
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
        # msgBox.setStandardButtons(
        #     msgBox.StandardButton.Ok |
        #     msgBox.StandardButton.Cancel
        # )

        # msgBox.button(msgBox.StandardButton.Cancel).setText('Cancelar')

        # result = msgBox.exec()

        # if result == msgBox.StandardButton.Ok:
        #     print('Usuario clicou em OK')

        # if result == msgBox.StandardButton.Cancel:
        #     print('Usuario clicou em Cancel')

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setInformativeText('''Texto absurdamente enorme''')
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()
        