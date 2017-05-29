from collections import defaultdict

from nwmatcher import NWMatcher


class Vocabulary:
    def __init__(self):
        self.dict = defaultdict(lambda: False)

    @staticmethod
    def cmp(s, t):
        n = min(len(s), len(t))
        m = 0
        for i in range(n):
            if s[i] != t[i]:
                break
            m += 1
        return m

    def init_dict(self, voc_file):
        f = open(voc_file, 'r')
        for line in f:
            tmp_line = line.strip()
            if not self.dict[tmp_line]:
                self.dict[tmp_line] = True

    def search(self, word):
        is_word = self.dict[word.strip()]
        if not is_word:
            self.dict.pop(word)
        return is_word

    def predict(self, word):
        word = word.strip()
        m = len(word)
        if m < 2:
            return []

        nw = NWMatcher()
        result_dict = {}

        for item in self.dict:
            if not m - 2 < len(item) < m + 2:
                continue
            result_dict[item] = nw.match(word, item)

        # sort by score
        result_list = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

        # only want items with highest score
        optimal = []
        for i in range(len(result_list)):
            if result_list[i][1] != result_list[0][1]:
                break
            optimal.append(result_list[i][0])

        # get the best one
        best = ''
        likelihood = 0
        for i in range(len(optimal)):
            score = self.cmp(word, optimal[i])
            if score > likelihood:
                likelihood = score
                best = optimal[i]

        return best


if __name__ == '__main__':
    voc = Vocabulary()
    voc.init_dict('wordlist')

    iw = input('> ')
    while iw != 'q':
        if not voc.search(iw):
            print('wrong, maybe', voc.predict(iw))

        iw = input('> ')
