import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QApplication, QLayout, QPushButton, \
    QMessageBox

from ranking import Ranking


class RankView(QWidget):
    def __init__(self, user_name, rank_data, ranking, success, parent=None):
        super().__init__(parent)
        self.rank_data = rank_data
        self.success = success
        self.ranking = ranking
        self.setWindowTitle('게임 결과')

        self.rank_slot = QTextEdit()
        self.rank_slot.setReadOnly(True)

        for i in range(len(rank_data)):
            if i < 3:
                rank_user = rank_data[i][0]
                rank_record = rank_data[i][1]
                self.rank_slot.append(str(i + 1) + ". " + rank_user + ": " + str(rank_record))

        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.layout.addWidget(self.rank_slot)

        self.layout.addSpacing(20)

        self.result_text = QLabel("[ 성공! ]") if success else QLabel("[ 실패... ]")
        self.result_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_text)

        self.layout.addSpacing(20)

        self.name_text = QLabel("이름: " + str(user_name))
        self.name_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.name_text)

        if success:
            self.rank_text = QLabel("등수: 1")
            self.rank_text.setAlignment(Qt.AlignCenter)
            self.record_text = QLabel("기록: 1000")
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
                self.ranking.rank_data = self.rank_data
                self.ranking.write_to_file()
            sys.exit()
        else:
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ranking = Ranking()
    ranking.read_from_file()
    print("# rank_data =", ranking.rank_data)
    rank_view = RankView(user_name='test', rank_data=[('test1', 1000), ('test2', 100)], success=True, ranking=ranking)
    rank_view.show()
    sys.exit(app.exec_())
