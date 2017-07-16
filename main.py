from optparse import OptionParser

from vocabulary import Vocabulary

alphabet = 'abcdefghijklmnopqrstuvwxyz'
split_chars = ' \n?,.'


def parse(file_name):
    """
    parse input file to get all the words and their positions
    :param file_name: input file
    :return: parsed word list
    """
    word_list = []
    with open(file_name, 'r') as file:
        tmp_word = ''
        index = 0
        last = ''
        c = file.read(1).lower()
        while c != '':
            if c in alphabet:
                tmp_word += c
            elif c in split_chars:
                if last in alphabet:
                    word_list.append([tmp_word, index - len(tmp_word), 0, ''])
                    tmp_word = ''

            last = c
            index += 1
            c = file.read(1)

    return word_list


def analyse(word_list, num_advice):
    """
    analyse words in word_list with vocabulary class
    :param word_list: word list
    :param num_advice: number of advice to provide
    :return: none
    """
    voc = Vocabulary()
    voc.init_dict('wordlist')

    for i in range(len(word_list)):
        if not voc.search(word_list[i][0]):
            word_list[i][2] = 1
            word_list[i][3] = voc.predict(word_list[i][0], num_advice)


def write_back(i_file, o_file, word_list):
    """
    write analysed word_list to output file with extra information (auto-correction)
    :param i_file: input file
    :param o_file: output file
    :param word_list: analysed word list
    :return: none
    """
    with open(i_file, 'r') as f:
        content = list(f.read())

    offset = 0
    count = 0
    with open(o_file, 'w') as f:
        for item in word_list:
            if item[2] == 0:
                continue

            preds = ''
            for i in range(len(item[3]) - 1):
                preds += item[3][i]
                preds += ','
            preds += item[3][len(item[3]) - 1]

            content.insert(item[1] + offset, '#')
            content.insert(item[1] + offset + len(item[0]) + 1, '({})'.format(preds))

            offset += 2
            count += 1

        for c in content:
            f.write(c)
        f.flush()

        print("errors: {}".format(count))


def parse_opt():
    """
    parse console options
    :return: parsed options
    """
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="input.txt",
                      type="string", help="input file to handle")
    parser.add_option("-o", "--output", dest="output", default="output.txt",
                      type="string", help="output file of result")
    parser.add_option("-n", "--num_advice", dest="num_advice", default=1,
                      type="int", help="number of advice word to provide")
    (options, args) = parser.parse_args()

    return options


if __name__ == '__main__':
    # parse console options
    opts = parse_opt()

    # assign file names
    in_file = opts.input
    out_file = opts.output

    # parse input file
    w_list = parse(in_file)
    # analyse parsed word list
    analyse(w_list, opts.num_advice)
    # write results to output file
    write_back(in_file, out_file, w_list)
