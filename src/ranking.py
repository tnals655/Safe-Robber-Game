import pickle


class Ranking:
    def __init__(self):
        self.file_name = 'ranking.dat'
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

    def rank_to_data(self, user_name, time):
        self.rank_data.append((user_name, time))
        self.rank_data = sorted(self.rank_data, reverse=True)


if __name__ == '__main__':
    ranking = Ranking()
    ranking.read_from_file()
    ranking.rank_to_data('test', 10)
    ranking.rank_to_data('test1', 111)
    ranking.rank_to_data('abc', 1)
    print(ranking.rank_data)
    ranking.write_to_file()
