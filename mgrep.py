# coding: utf-8
import logging
from re import match

from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()
IGNORE_WORDS = {
    'весь', 'всё', 'её', 'каждый', 'какой', 'который', 'мой', 'он', 'они', 'такой', 'твой', 'то', 'тот',
    'это', 'этот', 'сам'
}
IGNORE_PHRASES = [['доброе', 'утро']]


def morph(parsed, grammems, form):
    for word in parsed:
        if form not in word.tag or word.score < 0.1:
            continue
        for lexeme in word.lexeme:
            if lexeme.normal_form in IGNORE_WORDS:
                return
            if 'Name' in lexeme.tag:
                continue
            if all(grammem in lexeme.tag for grammem in grammems | {form}):
                return lexeme.word.capitalize()


def add_common_tag(words, category, tags):
    for tag in category:
        if all(any(tag in w.tag for w in word) for word in words):
            tags.add(tag)
            return True


def morphs(words):
    parsed = list(map(morpher.parse, words))
    grammems = {'nomn'}  # стараемся привести всё к именительному падежу
    # Обеспечиваем согласованность по числу, множественное в приоритете
    if not add_common_tag(parsed, ('plur', 'sing'), grammems):
        return [None]
    if 'sing' in grammems:  # И, в случае единственного числа, по полу
        add_common_tag(parsed, ('masc', 'femn', 'neut'), grammems)
    return morph(parsed[0], grammems, 'ADJF'), morph(parsed[1], grammems, 'NOUN')


def pick_combos(line):
    words = line.lower().split()
    combos = [words[i:i + 2] for i in range(len(words) - 1)]
    for combo in combos:
        if not all(match('^[а-я]+$', word) and len(word) > 1 for word in combo):
            continue
        if combo not in IGNORE_PHRASES and all(words := morphs(combo)):
            yield " ".join(words)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
    for i in pick_combos("по крайней мере"):
        print(i)
