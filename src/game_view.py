from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QDial, QLCDNumber, QLabel
from PyQt5.QtCore import Qt
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
        self.result_lcd = QLCDNumber(self)
        self.result_lcd.setDigitCount(6)
        self.result_lcd.setFixedSize(300, 100)
        self.result_lcd.setBaseSize(300, 100)
        self.result_lcd.setMinimumSize(200, 100)
        self.result_lcd.display('000000')

        self.page_display = QLineEdit()
        self.page_display.setText('버튼을 누르는 횟수 : ' + "'" +  str(self.game.max_page) + "'" + ' 번')
        self.page_display.setAlignment(Qt.AlignCenter)
        self.page_display.setReadOnly(True)


        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(1, 30)
        self.dial.setValue(0)
        self.dial.setWrapping(False)
        # self.dial.valueChanged[int].connect(self.chagne_Value) #다이얼 움직일때 소리 함수와 연결
        self.dial.valueChanged[int].connect(self.value_changed)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.button_clicked)  # next 버튼 누르면 result_edit 에 입력

        # 레이아웃
        self.result_layout = QHBoxLayout()
        self.result_layout.addStretch(3)
        self.result_layout.addWidget(self.result_lcd)
        self.result_layout.addStretch(3)

        self.page_display_layout = QHBoxLayout()
        self.page_display_layout.addWidget(self.page_display)

        self.next_button_layout = QHBoxLayout()
        self.next_button_layout.addStretch(1)
        self.next_button_layout.addWidget(self.next_button)
        self.next_button_layout.addStretch(1)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.result_layout)
        self.main_layout.addLayout(self.page_display_layout)
        self.main_layout.addWidget(self.dial)
        self.main_layout.addLayout(self.next_button_layout)

        self.setLayout(self.main_layout)

        self.setWindowTitle("금고털기 게임")
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.move(300, 300)
        self.resize(400, 418)
        self.show()

    def button_clicked(self):
        button = self.sender()
        num = self.dial.value()
        page = self.game.current_page
        current_pw = self.game.goto_next(num)
        zeros = 6 - len(current_pw)  # 0의 개수
        display_pw = current_pw + '0' * zeros

        self.result_lcd.display(str(display_pw))

        # 마지막 페이지일 떄는 버튼 텍스트 'OK'로 변경
        if page >= self.game.max_page-1:
            button.setText("OK")
        # 페이지가 끝까지 가지 않았을 때 6자리가 되면 실패로 처리
        if len(current_pw) == 6:
            success = False

            if page >= self.game.max_page:
                success = self.game.check_password()

            self.game.record_time()
            self.rank_view = RankView(self.game, success=success)
            self.rank_view.show()
            self.hide()

    def value_changed(self, value):
        self.game.play_beep_sound(value)

    def update_game(self):
        max_page = self.game.max_page if self.game.difficulty == 'Easy' else '?'

        self.dial.setRange(1, self.game.max_number)
        self.page_display.setText('버튼을 누르는 횟수 : ' + "'" + str(max_page) + "'" + ' 번')
