import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QDial, QLCDNumber
from PyQt5.QtCore import Qt
from game import Game
from rank_view import RankView


class GameView(QWidget):

    def __init__(self, game_data):
        super().__init__(parent=None)
        self.game = game_data
        self.rank_view = QWidget()
        self.rank_view.hide()
        self.initUI()

    def initUI(self):
        # 버튼 생성
        #self.result_edit.setAlignment(Qt.AlignRight)
        #self.result_edit.setReadOnly(True)
        #self.result_edit.setText('000000')

        self.result_lcd = QLCDNumber(self)
        self.result_lcd.setDigitCount(6)
        self.result_lcd.setFixedSize(300, 100)
        self.result_lcd.setBaseSize(300, 100)
        self.result_lcd.setMinimumSize(200, 100)
        self.result_lcd.display('000000')

        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0, 40)
        self.dial.setValue(0)
        self.dial.setWrapping(False)
        # self.dial.valueChanged[int].connect(self.chagne_Value) #다이얼 움직일때 소리 함수와 연결

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.button_clicked)  # ok버튼 누르면 result_edit에 입력

        # 레이아웃
        self.result_layout = QHBoxLayout()
        self.result_layout.addStretch(3)
        self.result_layout.addWidget(self.result_lcd)
        self.result_layout.addStretch(3)

        self.ok_layout = QHBoxLayout()
        self.ok_layout.addStretch(1)
        self.ok_layout.addWidget(self.ok_button)
        self.ok_layout.addStretch(1)

        self.window2_layout = QVBoxLayout()
        # self.window2_layout.addStretch(1)
        self.window2_layout.addLayout(self.result_layout)
        self.window2_layout.addWidget(self.dial)
        self.window2_layout.addLayout(self.ok_layout)

        self.setLayout(self.window2_layout)

        self.setWindowTitle("금고털기 게임")  # 윈도우 크기상 두글자가 최대
        self.move(300, 300)
        self.resize(418, 418)
        self.show()  # show를 initUI에다가

    def button_clicked(self): #수정함
        num = self.dial.value()
        page = self.game.current_page
        current_pw = self.game.goto_next(num)
        zeros = 6 - len(current_pw)  # 0의 개수
        display_pw = current_pw + '0' * zeros
        #self.result_edit.setText(display_pw)
        self.result_lcd.display(str(display_pw))
        # game.py의 goto_next 에 현재 입력값을 넣어서 game.py의 current_pw 갱신
        if page >= self.game.max_page:
            self.game.record_time()
            self.rank_view = RankView(self.game, success=self.game.check_password())
            self.rank_view.show()
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_instance = Game()
    game_instance.new_game(user_name='test', difficulty='Hard')
    game_view = GameView(game_instance)
    sys.exit(app.exec_())
