import random
import sys
import time
import winsound

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication

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
        return self.current_pw, self.current_page

    def play_sound_test(answer, value):  # 30씩 증가
        answer_fr = 1000
        duration = 1500
        if answer > value:
            play_fr = answer_fr - 30 * (answer - value)
        else:
            play_fr = answer_fr - 30 * (value - answer)
        print(play_fr)
        winsound.Beep(play_fr, duration)

def play_beep_sound(): #winsound.Beep(frequency, duration) 37Hz~32,767Hz milliseconds
    fr = 2000  # range : 37 ~ 32767
    du = 1000  # 1000 ms ==1second
    winsound.Beep(fr, du)
    # 0~value: 커지다가 vale~30: 줄어들게



if __name__ == '__main__':
    play_beep_sound()