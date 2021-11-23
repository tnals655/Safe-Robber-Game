import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QRadioButton, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from game import Game
from game_view import GameView


class UserInfoView(QWidget):

    def __init__(self, game_data):
        super().__init__()
        self.initUI()
        self.game = game_data
        self.game_view = GameView(self.game)
        self.game_view.hide()
        # self.game_view = GameView()

    # 버튼 생성

    def initUI(self):
        self.game_label = QLabel('플레이어 정보 입력', self)

        self.name_label = QLabel('이름', self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setMaxLength(10)

        self.backspace_error = QLabel('(입력에 문제가 발생했다면 \'ESC\' 키를 눌러주세요)', self)

        self.difficulty_label = QLabel('난이도', self)

        self.easy_radio = QRadioButton('Easy', self)
        self.hard_radio = QRadioButton('Hard', self)
        self.easy_radio.setChecked(True)

        self.start_button = QPushButton('시작', self)  # self.button.clicked.connect(self.button_clicked)
        self.start_button.clicked.connect(self.button_clicked)  # addButton.clicked.connect(self.btnAdd_Clicked)

        # 레이아웃
        self.game_layout = QHBoxLayout()
        self.game_layout.addStretch(1)
        self.game_layout.addWidget(self.game_label)
        self.game_layout.addStretch(1)

        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_edit)

        self.difficulty_layout = QHBoxLayout()
        self.difficulty_layout.addWidget(self.easy_radio)
        self.difficulty_layout.addWidget(self.hard_radio)

        self.start_layout = QHBoxLayout()
        self.start_layout.addWidget(self.start_button)

        # 위 레이아웃들 윈도우에 대입.
        self.window1_layout = QVBoxLayout()
        self.window1_layout.addStretch(1)
        self.window1_layout.addLayout(self.game_layout)
        self.window1_layout.addStretch(1)
        self.window1_layout.addLayout(self.name_layout)
        self.window1_layout.addWidget(self.backspace_error)
        self.window1_layout.addStretch(1)
        self.window1_layout.addWidget(self.difficulty_label)
        self.window1_layout.addLayout(self.difficulty_layout)
        self.window1_layout.addStretch(1)
        self.window1_layout.addLayout(self.start_layout)

        self.setLayout(self.window1_layout)

        # 윈도우
        self.setWindowTitle("금고 털기 게임")
        self.move(300, 300)
        self.resize(400, 220)
        self.show()  # show를 initUI에다가

    def button_clicked(self):
        self.user_name = self.name_edit.text().strip()
        if len(self.user_name) == 0:
            QMessageBox.about(self, "ERROR: name", "이름을 입력하세요")
        else:
            difficulty = 'Easy' if self.easy_radio.isChecked() else 'Hard'
            self.game.new_game(self.user_name, difficulty)
            self.game_view.show()
            self.hide()





if __name__ == '__main__':
    game = Game()
    app = QApplication(sys.argv)
    ex = UserInfoView(game)
    sys.exit(app.exec_())
