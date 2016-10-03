# coding: utf-8
import sys
from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()


def choose_suitable_form(parsed, grammem):
    for word in parsed:
        if grammem in word.tag and u'nomn' in word.tag:
            return word.word


def validate(words):
    parsed = (
        choose_suitable_form(morpher.parse(words[0]), u'ADJF'),
        choose_suitable_form(morpher.parse(words[1]), u'NOUN'),
    )
    return all(parsed) and parsed


def process_line(line):
    words = line.lower().split()
    combos = [words[i:i + 2] for i in range(len(words) - 1)]
    for i in combos:
        try:
            result = validate(i)
            if result:
                return u" ".join(result)
        except:
            pass


if __name__ == '__main__':
    process_line(unicode(" ".join(sys.argv[1:]), 'utf-8'))
