import random

MIN_NUMBER = 1
MAX_NUMBER = 30


class Game:
    def __init__(self, user_name, difficulty):
        self.answer_list = []
        self.user_name = user_name
        self.difficulty = difficulty
        self.current_pw = '000000'
        self.max_page = random.randrange(3, 7)
        self.current_page = 1
        self.answer_text = self.create_password()

    # 정답 결정
    def create_password(self):
        for i in range(self.max_page):
            rand_num = random.randrange(1, 10)

            if self.max_page == 3:
                rand_num = random.randrange(10, MAX_NUMBER + 1)
            elif self.max_page == 4:
                rand_num = random.randrange(1, 10) if i < 2 else random.randrange(10, MAX_NUMBER + 1)
            elif self.max_page == 5:
                rand_num = random.randrange(1, 10) if i > 0 else random.randrange(10, MAX_NUMBER + 1)

            self.answer_list.append(rand_num)

        result_text = ''

        for num in self.answer_list:
            result_text += str(num)

        print("# answer_list:", self.answer_list)

        return result_text

    # 정답 체크
    def check_password(self, password):
        return password == self.answer_text


if __name__ == '__main__':
    game = Game('test', 'EASY')
    print("# answer_text:", game.answer_text)
    print("# max_page:", game.max_page)
