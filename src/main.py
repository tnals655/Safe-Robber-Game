import sys

from PyQt5.QtWidgets import QApplication

from game import Game
from user_info_view import UserInfoView


def main():
    app = QApplication(sys.argv)
    game = Game()
    user_info_view = UserInfoView(game)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
