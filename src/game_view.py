import sys
import winsound

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QDial, QLCDNumber, QLabel
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

        # if 난이도가 easy
        self.easy_mode = QLineEdit()
        self.easy_mode.setText('버튼을 누르는 횟수 : ' + "'" +  str(self.game.max_page) + "'" + ' 번')
        self.easy_mode.setAlignment(Qt.AlignCenter)
        self.easy_mode.setReadOnly(True)


        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(1, 30)
        self.dial.setValue(0)
        self.dial.setWrapping(False)
        #self.dial.valueChanged.connect(self.play_sound)
        # self.dial.valueChanged[int].connect(self.chagne_Value) #다이얼 움직일때 소리 함수와 연결
        self.dial.valueChanged[int].connect(self.value_changed)

        self.ok_button = QPushButton('Next', self)
        self.ok_button.clicked.connect(self.button_clicked)  # ok 버튼 누르면 result_edit 에 입력

        # 레이아웃
        self.result_layout = QHBoxLayout()
        self.result_layout.addStretch(3)
        self.result_layout.addWidget(self.result_lcd)
        self.result_layout.addStretch(3)

        self.easy_mode_layout = QHBoxLayout()
        self.easy_mode_layout.addWidget(self.easy_mode)

        self.ok_layout = QHBoxLayout()
        self.ok_layout.addStretch(1)
        self.ok_layout.addWidget(self.ok_button)
        self.ok_layout.addStretch(1)

        self.window2_layout = QVBoxLayout()
        self.window2_layout.addLayout(self.result_layout)
        if self.game.difficulty == 'Easy':  # 난이도가 Easy 일 때 버튼을 누르는 횟수를 알려주는 QLineEdit() 추가
            self.window2_layout.addLayout(self.easy_mode_layout)
        self.window2_layout.addWidget(self.dial)
        self.window2_layout.addLayout(self.ok_layout)

        self.setLayout(self.window2_layout)

        self.setWindowTitle("금고털기 게임")
        self.setWindowIcon(QIcon('resources/icon.png'))# 윈도우 크기상 두글자가 최대
        self.move(300, 300)
        self.resize(400, 418)
        self.show()  # show를 initUI에다가

    def button_clicked(self):
        button = self.sender()
        num = self.dial.value()
        page = self.game.current_page
        current_pw = self.game.goto_next(num)
        zeros = 6 - len(current_pw)  # 0의 개수
        display_pw = current_pw + '0' * zeros
        #self.result_edit.setText(display_pw)
        self.result_lcd.display(str(display_pw))

        # 마지막 페이지일 떄는 버튼 텍스트 'OK'로 변경
        if page >= self.game.max_page-1:
            button.setText("OK")
        # game.py의 goto_next 에 현재 입력값을 넣어서 game.py의 current_pw 갱신
        # 페이지가 끝까지 가지 않았을 때 6자리가 되면 실패로 처리
        if len(current_pw) == 6:
            success = self.game.check_password() if page >= self.game.max_page else False
            self.game.record_time()
            self.rank_view = RankView(self.game, success=success)
            self.rank_view.show()
            self.hide()

    def value_changed(self, value):
        self.game.play_beep_sound(value)

    def update_dial_range(self):
        self.dial.setRange(1, self.game.max_number)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_instance = Game()
    game_instance.new_game(user_name='test', difficulty='Hard')
    game_view = GameView(game_instance)
    sys.exit(app.exec_())

