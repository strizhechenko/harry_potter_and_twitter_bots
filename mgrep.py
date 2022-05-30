# coding: utf-8
import logging
import re

from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()
IGNORE_WORDS = {
    'весь', 'всё', 'её', 'каждый', 'какой', 'такой', 'который', 'мой', 'он', 'они', 'твой', 'то', 'тот',
    'это', 'этот', 'сам'
}
IGNORE_PHRASES = [['доброе', 'утро']]


def morph(parsed: list, grammems: set, form: str) -> str or None:
    for word in parsed:
        if form in word.tag and word.score > 0.1:
            for lexeme in word.lexeme:
                if lexeme.normal_form in IGNORE_WORDS:
                    return
                if 'Name' not in lexeme.tag:
                    if all(grammem in lexeme.tag for grammem in grammems | {form}):
                        return lexeme.word.capitalize()


def add_common_tag(words: list, category: tuple, tags: set) -> bool or None:
    for tag in category:
        if all(any(tag in w.tag for w in word) for word in words):
            tags.add(tag)
            return True


def morphs(words: tuple) -> tuple:
    parsed = list(map(morpher.parse, words))
    grammems = {'nomn'}  # стараемся привести всё к именительному падежу
    # Обеспечиваем согласованность по числу, множественное в приоритете
    if not add_common_tag(parsed, ('plur', 'sing'), grammems):
        return None, None  # нужно для работы all(result := )
    if 'sing' in grammems:  # И, в случае единственного числа, по полу
        add_common_tag(parsed, ('masc', 'femn', 'neut'), grammems)
    return morph(parsed[0], grammems, 'ADJF'), morph(parsed[1], grammems, 'NOUN')


def pick_combos(line: str):
    words = line.lower().split()
    for n, word in enumerate(words[1:], 1):
        combo = (words[n - 1], word)
        if all(re.match('^[а-я]{2,}$', word) for word in combo) and combo not in IGNORE_PHRASES:
            if all(result := morphs(combo)):
                yield " ".join(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
    for i in pick_combos("по крайней мере"):
        print(i)
