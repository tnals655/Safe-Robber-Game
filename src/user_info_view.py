import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QRadioButton, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMessageBox, QTextEdit, QFrame
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

        self.difficulty_label = QLabel('<난이도>', self)
        self.easy_explain_label = QLabel('※ Easy : 버튼을 눌러야 하는 횟수가 게임 창에 표시됩니다.', self)
        self.hard_explain_label = QLabel('※ Hard : 소리로만 정답을 유추해야 합니다.', self)

        self.rule_label = QLabel("<게임 설명>")
        self.rule_label.setAlignment(Qt.AlignCenter)

        self.rule_edit = QTextEdit()
        self.rule_edit.setReadOnly(True)
        self.rule_edit.setAutoFillBackground(False)
        self.rule_edit.setFrameStyle(QFrame.Plain)
        self.rule_edit.setAlignment(Qt.AlignLeft)
        self.rule_edit.setMinimumSize(350, 100)
        self.rule_edit.append("금고털기 게임은 여러 개의 숫자를 조합해서 미리 정해진 6자리 숫자를 빨리 맞추는 게임입니다.")
        self.rule_edit.append("")
        self.rule_edit.append("다이얼에서 정답에 가까운 숫자로 향할수록 소리의 볼륨이 줄어듭니다.")
        self.rule_edit.append("")
        self.rule_edit.append("조합할 수 있는 숫자의 개수('Next' 버튼을 누르는 횟수)는 미리 정해져 있습니다.")
        self.rule_edit.append("")
        self.rule_edit.append("번호를 맞추는 데 성공하면 게임 진행 시간이 기록되며, 본인의 랭킹이 표시됩니다.")

        self.window2_layout = QVBoxLayout()
        self.window2_layout.addWidget(self.rule_label)
        self.window2_layout.addWidget(self.rule_edit)

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
        self.window1_layout.addWidget(self.easy_explain_label)
        self.window1_layout.addWidget(self.hard_explain_label)
        self.window1_layout.addStretch(1)
        self.window1_layout.addLayout(self.difficulty_layout)
        self.window1_layout.addStretch(1)
        self.window1_layout.addLayout(self.start_layout)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.window1_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.window2_layout)

        self.setLayout(self.main_layout)

        # 윈도우
        self.setWindowTitle("금고 털기 게임")
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.move(300, 300)
        self.resize(450, 320) #가로, 세로
        self.show()  # show를 initUI에다가

    def button_clicked(self):
        user_name = self.name_edit.text().strip()
        if len(user_name) == 0:
            QMessageBox.about(self, "ERROR: name", "이름을 입력하세요")
        else:
            difficulty = 'Easy' if self.easy_radio.isChecked() else 'Hard'
            self.game.new_game(user_name, difficulty)
            self.game_view.update_game()
            self.game_view.show()
            self.hide()





if __name__ == '__main__':
    game = Game()
    app = QApplication(sys.argv)
    ex = UserInfoView(game)
    sys.exit(app.exec_())
