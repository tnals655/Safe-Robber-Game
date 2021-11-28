from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QRadioButton, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMessageBox, QTextEdit, QFrame
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
        self.title_label = QLabel('플레이어 정보 입력', self)

        self.name_label = QLabel('이름', self)
        self.name_input = QLineEdit(self)
        self.name_input.setMaxLength(10)

        self.backspace_error_label = QLabel('(입력에 문제가 발생했다면 \'ESC\' 키를 눌러주세요)', self)

        self.difficulty_label = QLabel('<난이도>', self)
        self.easy_explain_label = QLabel('※ Easy : 버튼을 눌러야 하는 횟수가 게임 창에 표시됩니다.', self)
        self.hard_explain_label = QLabel('※ Hard : 소리로만 정답을 유추해야 합니다.', self)

        self.rule_label = QLabel("<게임 설명>")
        self.rule_label.setAlignment(Qt.AlignCenter)

        self.rule_display = QTextEdit()
        self.rule_display.setReadOnly(True)
        self.rule_display.setAutoFillBackground(False)
        self.rule_display.setFrameStyle(QFrame.Plain)
        self.rule_display.setAlignment(Qt.AlignLeft)
        self.rule_display.setMinimumSize(350, 100)
        self.rule_display.append("금고털기 게임은 여러 개의 숫자를 조합해서 미리 정해진 6자리 숫자를 빨리 맞추는 게임입니다.")
        self.rule_display.append("")
        self.rule_display.append("다이얼에서 정답에 가까운 숫자로 향할수록 소리의 볼륨이 줄어듭니다.")
        self.rule_display.append("")
        self.rule_display.append("조합할 수 있는 숫자의 개수('Next' 버튼을 누르는 횟수)는 미리 정해져 있습니다.")
        self.rule_display.append("")
        self.rule_display.append("번호를 맞추는 데 성공하면 게임 진행 시간이 기록되며, 본인의 랭킹이 표시됩니다.")

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.rule_label)
        self.right_layout.addWidget(self.rule_display)

        self.easy_radio = QRadioButton('Easy', self)
        self.hard_radio = QRadioButton('Hard', self)
        self.easy_radio.setChecked(True)

        self.start_button = QPushButton('시작', self)  # self.button.clicked.connect(self.button_clicked)
        self.start_button.clicked.connect(self.button_clicked)  # addButton.clicked.connect(self.btnAdd_Clicked)

        # 레이아웃
        self.title_layout = QHBoxLayout()
        self.title_layout.addStretch(1)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(1)

        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)

        self.difficulty_layout = QHBoxLayout()
        self.difficulty_layout.addWidget(self.easy_radio)
        self.difficulty_layout.addWidget(self.hard_radio)

        self.start_layout = QHBoxLayout()
        self.start_layout.addWidget(self.start_button)

        # 위 레이아웃들 윈도우에 대입.
        self.left_layout = QVBoxLayout()
        self.left_layout.addStretch(1)
        self.left_layout.addLayout(self.title_layout)
        self.left_layout.addStretch(1)
        self.left_layout.addLayout(self.name_layout)
        self.left_layout.addWidget(self.backspace_error_label)
        self.left_layout.addStretch(1)
        self.left_layout.addWidget(self.difficulty_label)
        self.left_layout.addWidget(self.easy_explain_label)
        self.left_layout.addWidget(self.hard_explain_label)
        self.left_layout.addStretch(1)
        self.left_layout.addLayout(self.difficulty_layout)
        self.left_layout.addStretch(1)
        self.left_layout.addLayout(self.start_layout)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

        # 윈도우
        self.setWindowTitle("금고 털기 게임")
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.move(300, 300)
        self.resize(450, 320) #가로, 세로
        self.show()  # show를 initUI에다가

    def button_clicked(self):
        user_name = self.name_input.text().strip()
        if len(user_name) == 0:
            QMessageBox.about(self, "ERROR: name", "이름을 입력하세요")
        else:
            difficulty = 'Easy' if self.easy_radio.isChecked() else 'Hard'
            self.game.new_game(user_name, difficulty)
            self.game_view.update_game()
            self.game_view.show()
            self.hide()
