import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QMessageBox

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Создаем поле ввода и добавляем его на соответствующий слой
        self.input = QLineEdit(self)
        self.grid.addWidget(self.input, 0, 0, 1, 4)

        # Создаем кнопки с цифрами и добавляем их на соответствующие слои
        self.b_1 = QPushButton("1", self)
        self.grid.addWidget(self.b_1, 1, 0)

        self.b_2 = QPushButton("2", self)
        self.grid.addWidget(self.b_2, 1, 1)

        self.b_3 = QPushButton("3", self)
        self.grid.addWidget(self.b_3, 1, 2)

        self.b_4 = QPushButton("4", self)
        self.grid.addWidget(self.b_4, 2, 0)

        self.b_5 = QPushButton("5", self)
        self.grid.addWidget(self.b_5, 2, 1)

        self.b_6 = QPushButton("6", self)
        self.grid.addWidget(self.b_6, 2, 2)

        self.b_7 = QPushButton("7", self)
        self.grid.addWidget(self.b_7, 3, 0)

        self.b_8 = QPushButton("8", self)
        self.grid.addWidget(self.b_8, 3, 1)

        self.b_9 = QPushButton("9", self)
        self.grid.addWidget(self.b_9, 3, 2)

        self.b_0 = QPushButton("0", self)
        self.grid.addWidget(self.b_0, 4, 1)

        self.b_dot = QPushButton(".", self)
        self.grid.addWidget(self.b_dot, 4, 0)

        # Создаем кнопки с операторами и добавляем их на соответствующие слои
        self.b_plus = QPushButton("+", self)
        self.grid.addWidget(self.b_plus, 1, 3)

        self.b_minus = QPushButton("-", self)
        self.grid.addWidget(self.b_minus, 2, 3)

        self.b_multiply = QPushButton("*", self)
        self.grid.addWidget(self.b_multiply, 3, 3)

        self.b_divide = QPushButton("/", self)
        self.grid.addWidget(self.b_divide, 4, 3)

        self.b_result = QPushButton("=", self)
        self.grid.addWidget(self.b_result, 4, 2)

        # Подключаем обработчики событий для каждой кнопки
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self.button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_dot.clicked.connect(lambda: self._button("."))
        self.b_plus.clicked.connect(lambda: self._button("+"))
        self.b_minus.clicked.connect(lambda: self._button("-"))
        self.b_multiply.clicked.connect(lambda: self._button("*"))
        self.b_divide.clicked.connect(lambda: self._button("/"))
        self.b_result.clicked.connect(self._calculate)
        # Устанавливаем параметры главного окна приложения
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('Mega Duper Super Calculator v 0.1 alpha beta - trash')
        self.show()

    # Метод для добавления символов к строке ввода при нажатии на соответствующие кнопки
    def _button(self, text):
        self.input.setText(self.input.text() + text)

    # Метод для выполнения вычисления выражения из строки ввода и вывода результата
    def _calculate(self):
        try:
            result = eval(self.input.text())
            self.input.setText(str(result))
        except ZeroDivisionError:
            QMessageBox.warning(self, "Внимание", "На ноль делить нельзя!")
        except:
            QMessageBox.warning(self, "Внимание", "Произошла ошибка!")

    def _operation(self, op):
        self.num_1 = int(self.input.text())
        self.op = op
        self.input.setText("")

    def _result(self):
        self.num_2 = int(self.input.text())
        if self.op == "+":
            self.input.setText(str(self.num_1 + self.num_2))

# Запуск приложения
app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())