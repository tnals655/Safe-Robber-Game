import random
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect


class Game:
    def __init__(self):
        self.answer_list = []
        self.user_name = ''
        self.difficulty = ''
        self.current_pw = ''
        self.max_page = 0
        self.current_page = 0
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile('resources/beep.wav'))
        self.start_time = -1
        self.time_record = -1
        self.max_number = 30

    # 새로운 게임 시작
    def new_game(self, user_name, difficulty):
        self.user_name = user_name
        self.difficulty = difficulty
        self.current_pw = ''
        self.max_page = random.randrange(3, 7)
        self.current_page = 1
        self.create_password()
        self.start_time = time.time()
        self.max_number = 30 if difficulty == 'Easy' else 40
        # print("# max_page:", self.max_page)

    # 정답 결정
    def create_password(self):
        global rand_num
        for i in range(self.max_page):

            if self.max_page == 3:
                rand_num = random.randrange(10, self.max_number + 1)
            elif self.max_page == 4:
                rand_num = random.randrange(1, 10) if i < 2 else random.randrange(10, self.max_number + 1)
            elif self.max_page == 5:
                rand_num = random.randrange(1, 10) if i > 0 else random.randrange(10, self.max_number + 1)

            self.answer_list.append(rand_num)

        random.shuffle(self.answer_list)  # 숫자 결정 후에 리스트 랜덤으로 섞기

    def get_password(self):
        result_text = ''

        for num in self.answer_list:
            result_text += str(num)

        #print("# answer_list:", self.answer_list)

        return result_text

    # 정답 체크
    def check_password(self):
        return self.current_pw == self.get_password()

    def record_time(self):
        self.time_record = time.time() - self.start_time

    def goto_next(self, value):
        self.current_pw += str(value)
        self.current_page += 1
        return self.current_pw

    def play_siren_sound(self):
        self.sound_effect.setSource(QUrl.fromLocalFile('resources/siren.wav'))
        self.sound_effect.setVolume(0.5)
        self.sound_effect.play()

    def play_beep_sound(self, value):
        answer = self.answer_list[self.current_page - 1]

        # 1 ~ answer 볼륨 감소
        if value <= answer:
            interval = 1 / answer
            volume = (1 - (interval * value))
        # answer ~ max 볼륨 증가
        else:
            interval = 1 / (self.max_number - answer)
            volume = (value - answer) * interval

        self.sound_effect.setVolume(volume)
        self.sound_effect.play()
