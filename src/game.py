import random
import sys
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect

MIN_NUMBER = 1
MAX_NUMBER = 30


class Game:
    def __init__(self):
        self.answer_list = []
        self.user_name = ''
        self.difficulty = ''
        self.current_pw = ''
        self.max_page = 0
        self.current_page = 0
        self.answer_text = ''
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile('resources/beep.wav'))
        self.start_time = -1
        self.time_record = -1

    # 새로운 게임 시작
    def new_game(self, user_name, difficulty):
        self.user_name = user_name
        self.difficulty = difficulty
        self.current_pw = ''
        self.max_page = random.randrange(3, 7)
        self.current_page = 1
        self.answer_text = self.create_password()
        self.start_time = time.time()
        #print("# max_page:", self.max_page)

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
    def check_password(self):
        return self.current_pw == self.answer_text

    def record_time(self):
        self.time_record = time.time() - self.start_time

    def goto_next(self, value):
        self.current_pw += str(value)
        self.current_page += 1
        return self.current_pw

    def play_beep_sound(self, value):
        # 0부터 answer까지 줄이다가 answer부터 30까지 늘리기
        answer = self.answer_list[self.current_page - 1]
        volume = (1 - (value / answer)) if answer >= value else (value - answer) / (MAX_NUMBER - answer)
        self.sound_effect.setVolume(volume)
        self.sound_effect.play()

