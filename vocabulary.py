from collections import defaultdict

from nwmatcher import NWMatcher


class Vocabulary:
    def __init__(self):
        self.dict = defaultdict(lambda: False)

    @staticmethod
    def cmp(s, t):
        """
        compare the likelihood of two words
        :param s: word 1
        :param t: word 2
        :return: likelihood
        """
        n = min(len(s), len(t))
        m = 0
        for i in range(n):
            if s[i] != t[i]:
                break
            m += 1
        return m

    def init_dict(self, voc_file):
        """
        initialize class owned dict with vocabulary file
        :param voc_file: vocabulary file
        :return:
        """
        f = open(voc_file, 'r')
        for line in f:
            tmp_line = line.strip()
            if not self.dict[tmp_line]:
                self.dict[tmp_line] = True

    def search(self, word):
        """
        search the word in the dict
        :param word: word to search
        :return: whether the word is in the dict
        """
        is_word = self.dict[word.strip()]
        if not is_word:
            self.dict.pop(word)
        return is_word

    def predict(self, word, num_advice):
        """
        predict the most likely correct words if word is incorrect
        :param word: word to predict
        :param num_advice: number of predictions to give
        :return: list of predictions
        """
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
        result_list = result_list[:50]

        # only want items with highest score
        optimal = []
        len_opt = 0
        for i in range(len(result_list)):
            if result_list[i][1] != result_list[0][1]:
                break
            optimal.append([result_list[i][0], 0])
            len_opt += 1

        # sort the optimal by likelihood
        for i in range(len(optimal)):
            optimal[i][1] = self.cmp(word, optimal[i][0])
        optimal.sort(key=lambda x: x[1], reverse=True)

        # the final list
        final = [x[0] for x in optimal]
        resdue = [x[0] for x in result_list[len_opt:]]
        final.extend(resdue)

        #length = min(num_advice, len(optimal))
        return [x for x in final[:num_advice]]


if __name__ == '__main__':
    voc = Vocabulary()
    voc.init_dict('wordlist')

    iw = input('> ')
    while iw != 'q':
        if not voc.search(iw):
            print('wrong, maybe', voc.predict(iw, 2))

        iw = input('> ')
