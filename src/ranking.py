import pickle


class Ranking:
    def __init__(self, difficulty):
        self.file_name = 'ranking_' + str(difficulty).lower() + '.dat'
        # List of Tuple (이름, 시간)
        self.rank_data = []

    def read_from_file(self):
        try:
            file = open(self.file_name, 'rb')
        except FileNotFoundError as e:
            self.rank_data = []
            return
        try:
            self.rank_data = pickle.load(file)
        except:
            pass
        else:
            pass
        file.close()

    def write_to_file(self):
        file = open(self.file_name, 'wb')
        pickle.dump(self.rank_data, file)
        file.close()

    def rank_data(self, user_name, time):
        self.rank_data.append((user_name, time))
        self.rank_data = sorted(self.rank_data)
