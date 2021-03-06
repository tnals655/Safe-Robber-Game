import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QApplication, QLayout, QPushButton, \
    QMessageBox

from ranking import Ranking


class RankView(QWidget):
    def __init__(self, game_data, success, parent=None):
        super().__init__(parent)
        self.game = game_data
        self.user_name = game_data.user_name
        self.difficulty = game_data.difficulty
        self.ranking = Ranking(self.difficulty)
        self.ranking.read_from_file()
        self.rank_data = self.ranking.rank_data
        self.success = success
        self.initUI()
        if not success:
            self.game.play_siren_sound()


    def initUI(self):
        # 랭킹
        self.rank_display = QTextEdit()
        self.rank_display.setReadOnly(True)
        for i in range(len(self.rank_data)):
            if i < 3:
                rank_user = self.rank_data[i][0]
                rank_record = self.rank_data[i][1]
                self.rank_display.append(str(i + 1) + ". " + rank_user + ": " + str(round(rank_record, 2)) + "초")

        # 공통 (성공/실패)
        self.result_label = QLabel("[ 성공! ]") if self.success else QLabel("[ 실패... ]")
        self.result_label.setAlignment(Qt.AlignCenter)

        self.name_text = QLabel("이름: " + str(self.user_name))
        self.name_text.setAlignment(Qt.AlignCenter)

        self.end_button = QPushButton('종료')
        self.end_button.clicked.connect(self.button_clicked)

        # 메인 레이아웃
        self.main_layout = QVBoxLayout()
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.main_layout.addWidget(self.rank_display)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.result_label)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.name_text)

        # 성공시 등수와 기록을 보여줌(레이아웃 추가)
        if self.success:
            # 랭킹 데이터 복사해서 플레이어 등수 구하기
            record_tuple = (self.user_name, self.game.time_record)
            temp_rank_data = self.ranking.rank_data.copy()
            temp_rank_data.append(record_tuple)
            temp_rank_data = sorted(temp_rank_data, key=lambda x: x[1])
            self.rank_label = QLabel("등수: " + str(temp_rank_data.index(record_tuple) + 1))
            self.rank_label.setAlignment(Qt.AlignCenter)

            self.record_label = QLabel("기록: " + str(round(self.game.time_record, 2)) + "초")
            self.record_label.setAlignment(Qt.AlignCenter)


            self.main_layout.addWidget(self.rank_label)
            self.main_layout.addWidget(self.record_label)
        else:
            self.my_answer_label = QLabel("내가 추측한 번호: " + self.game.current_pw)
            self.my_answer_label.setAlignment(Qt.AlignCenter)
            self.main_layout.addSpacing(20)
            self.main_layout.addWidget(self.my_answer_label)

        self.answer_label = QLabel("비밀번호: " + self.game.get_password())
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.answer_label)

        # 메인 레이아웃
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.end_button)

        self.setLayout(self.main_layout)

        self.setWindowTitle('게임 결과')
        self.setWindowIcon(QIcon('resources/icon.png'))

    def button_clicked(self):
        if self.success:
            ret = QMessageBox.question(self, '저장', '결과를 저장하겠습니까?', QMessageBox.Ok, QMessageBox.Cancel)
            if ret == QMessageBox.Ok:
                self.ranking.rank(user_name=self.user_name, time=self.game.time_record)
                self.ranking.write_to_file()
            sys.exit()
        else:
            sys.exit()

