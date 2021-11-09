class Game:
    def __init__(self, user_name, difficulty):
        self.user_name = user_name
        self.difficulty = difficulty
        self.current_pw = '000000'

        self.create_password()

    # 정답 결정
    def create_password(self):
        return '100000'

    # 정답 체크
    def check_password(self, password):
        return password == self.current_pw

