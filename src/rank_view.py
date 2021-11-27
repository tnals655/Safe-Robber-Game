import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QApplication, QLayout, QPushButton, \
    QMessageBox

from ranking import Ranking
from game import Game


class RankView(QWidget):
    def __init__(self, game_data, success, parent=None):
        super().__init__(parent)
        self.user_name = game_data.user_name
        self.difficulty = game_data.difficulty
        self.ranking = Ranking(self.difficulty)
        self.ranking.read_from_file()
        self.success = success
        self.setWindowTitle('게임 결과')
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.game = game_data

        self.rank_slot = QTextEdit()
        self.rank_slot.setReadOnly(True)

        rank_data = self.ranking.rank_data

        for i in range(len(rank_data)):
            if i < 3:
                rank_user = rank_data[i][0]
                rank_record = rank_data[i][1]
                self.rank_slot.append(str(i + 1) + ". " + rank_user + ": " + str(round(rank_record, 2)))

        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.layout.addWidget(self.rank_slot)

        self.layout.addSpacing(20)

        self.result_text = QLabel("[ 성공! ]") if success else QLabel("[ 실패... ]")
        self.result_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_text)

        self.layout.addSpacing(20)

        self.name_text = QLabel("이름: " + str(self.user_name))
        self.name_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.name_text)

        if success:
            record_tuple = (self.user_name, game_data.time_record)
            temp_rank_data = self.ranking.rank_data.copy()
            temp_rank_data.append(record_tuple)
            temp_rank_data.sort()
            self.rank_text = QLabel("등수: " + str(temp_rank_data.index(record_tuple) + 1))
            self.rank_text.setAlignment(Qt.AlignCenter)
            self.record_text = QLabel("기록: " + str(round(game_data.time_record, 2)))
            self.record_text.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.rank_text)
            self.layout.addWidget(self.record_text)

        self.layout.addSpacing(40)

        self.end_button = QPushButton('종료')
        self.end_button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.end_button)

        self.setLayout(self.layout)

    def button_clicked(self):
        if self.success:
            ret = QMessageBox.question(self, '저장', '결과를 저장하겠습니까?', QMessageBox.Ok, QMessageBox.Cancel)
            if ret == QMessageBox.Ok:
                self.ranking.rank_to_data(user_name=self.user_name, time=self.game.time_record)
                self.ranking.write_to_file()
            sys.exit()
        else:
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.new_game(user_name='test', difficulty='Easy')
    game.record_time()
    rank_view = RankView(game_data=game, success=True)
    rank_view.show()
    sys.exit(app.exec_())
