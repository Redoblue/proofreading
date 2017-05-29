from vocabulary import Vocabulary

alphabet = 'abcdefghijklmnopqrstuvwxyz'
split_chars = ' \n?,.'


def parse(file_name):
    word_list = []
    with open(file_name, 'r') as file:
        tmp_word = ''
        index = 0
        last = ''
        c = file.read(1).lower()
        while c != '':
            if c in alphabet:
                if last in split_chars:
                    tmp_word += c
                elif last in alphabet:
                    tmp_word += c
            elif c in split_chars:
                if last in alphabet:
                    word_list.append([tmp_word, index - len(tmp_word), 0, ''])
                    tmp_word = ''

            last = c
            index += 1
            c = file.read(1)

    return word_list


def analyse(w_list):
    voc = Vocabulary()
    voc.init_dict('wordlist')

    for i in range(len(w_list)):
        if not voc.search(w_list[i][0]):
            w_list[i][2] = 1
            w_list[i][3] = voc.predict(w_list[i][0])


def write_back(i_file, o_file, w_list):
    with open(i_file, 'r') as f:
        content = list(f.read())

    offset = 0
    with open(o_file, 'w') as f:
        for item in w_list:
            if item[2] == 0:
                continue
            else:
                content.insert(item[1] + offset, '#')
                content.insert(item[1] + offset + len(item[0]) + 1, '({})'.format(item[3]))
                offset += 2

        for c in content:
            f.write(c)
        f.flush()


if __name__ == '__main__':
    in_file = 'test'
    out_file = 'test.out'
    word_list = parse(in_file)
    analyse(word_list)
    write_back(in_file, out_file, word_list)
