import numpy as np


class NWMatcher:
    """
    class which implement the Needleman-Nunwh algorithm
    """
    def __init__(self, s='', t=''):
        self.s = s
        self.t = t
        self.opt = np.zeros((len(s) + 1, len(t) + 1), dtype=int)

    def match(self, s, t):
        """
        match two strings and return the final score
        :param s: string 1
        :param t: string 2
        :return: score
        """
        self.__init__(s, t)

        m = len(s) + 1
        n = len(t) + 1

        for i in range(m):
            self.opt[i, 0] = -3 * i
        for j in range(n):
            self.opt[0, j] = -3 * j

        for i in range(1, m):
            for j in range(1, n):
                if self.s[i - 1] == self.t[j - 1]:
                    d = 1
                else:
                    d = -1

                self.opt[i, j] = max(
                    self.opt[i - 1, j - 1] + d,
                    self.opt[i - 1, j] - 3,
                    self.opt[i, j - 1] - 3)

        return self.opt[m - 1, n - 1]

    def backtrack(self):
        """
        find the most possible case
        :return: the most possible case
        """
        i, j = len(self.s), len(self.t)
        a = b = ''

        while i != 0 or j != 0:
            if i == 0:
                j -= 1
                a += '-'
                b += self.t[j]
            elif j == 0:
                i -= 1
                a += self.s[i]
                b += '-'
            else:
                x, y, z = self.opt[i - 1, j - 1], self.opt[i - 1, j], self.opt[i, j - 1]
                if x >= y and x >= z:
                    i -= 1
                    j -= 1
                    ts = self.s[i]
                    tt = self.t[j]
                    if ts == tt:
                        a += ts
                        b += tt
                    else:
                        a += '*'
                        b += '*'
                elif y > z:
                    i -= 1
                    a += self.s[i]
                    b += '-'
                elif y < z:
                    j -= 1
                    a += '-'
                    b += self.t[j]
                else:
                    if i >= j:
                        i -= 1
                        a += self.s[i]
                        b += '-'
                    else:
                        j -= 1
                        a += '-'
                        b += self.s[j]

        return a[::-1], b[::-1]


if __name__ == '__main__':
    nw = NWMatcher()
    #print(nw.match('absense', 'absence'))
    print('goodds', 'gooedst')
    nw.match('goodds', 'gooedst')
    print(nw.opt)
    print(nw.backtrack())
