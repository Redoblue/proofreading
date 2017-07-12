from vocabulary import Vocabulary
import time


def k_find(v, word):
    result_list = v.predict(word, 50)
    return result_list


def main():
    voc = Vocabulary()
    voc.init_dict('wordlist')

    count_wrong = 0
    count_1 = 0
    count_5 = 0
    count_10 = 0
    count_25 = 0
    count_50 = 0

    with open('test.txt', 'r') as f:
        for line in f:
            words = line.strip().lower().split('\t')
            if voc.search(words[1]):
                count_wrong += 1

                result = k_find(voc, words[0])

                if words[1] == result[0]:
                    count_1 += 1
                if words[1] in result[:5]:
                    count_5 += 1
                if words[1] in result[:10]:
                    count_10 += 1
                if words[1] in result[:25]:
                    count_25 += 1
                if words[1] in result[:50]:
                    count_50 += 1

    print('Total: {}'.format(count_wrong))
    print('Total Found: {}'.format(count_50))
    print('Total Not Found: {}'.format(count_wrong - count_50))
    print('First: {}'.format(count_1 / count_wrong))
    print('1-5: {}'.format(count_5 / count_wrong))
    print('1-10: {}'.format(count_10 / count_wrong))
    print('1-25: {}'.format(count_25 / count_wrong))
    print('1-50: {}'.format(count_50 / count_wrong))


if __name__ == '__main__':
    time.clock()
    main()
    print('Total Time Cost: {}'.format(time.clock()))
