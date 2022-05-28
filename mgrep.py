# coding: utf-8
from re import match, UNICODE

from pymorphy2 import MorphAnalyzer

morpher = MorphAnalyzer()

BLACKLIST_WORDS = {
    'какой', 'какая', 'какое', 'какие',
    'такой', 'такая', 'такое', 'такие',
    'каждый', 'каждая', 'каждые', 'каждое',
    'который', 'которая', 'которые', 'которое',
    'этот', 'эта', 'это', 'эти',
    'весь', 'вся', 'всё', 'всю', 'все',
    'тот', 'та', 'то', 'те',
    'мой', 'моя', 'моё', 'мои',
    'твой', 'твоя', 'твоё', 'твои',
    'её', 'его', 'их'
}
BLACKLIST_COMBOS = [
    ['доброе', 'утро']
]


def morph(parsed, grammem):
    for word in parsed:
        if grammem in word.tag and 'nomn' in word.tag:
            return word.word.capitalize()


def morphs(words):
    return morph(morpher.parse(words[0]), 'ADJF'), morph(morpher.parse(words[1]), 'NOUN')


def pick_combos(line):
    words = line.lower().split()
    combos = [words[i:i + 2] for i in range(len(words) - 1)]
    for combo in combos:
        # Words aren't russian or too short
        if not all(match('^[а-я]+$', word, flags=UNICODE) and len(word) > 1 for word in combo):
            continue
        if combo in BLACKLIST_COMBOS:
            continue
        if any(word in BLACKLIST_WORDS for word in combo):
            continue
        words = morphs(combo)
        if not all(words):
            continue
        yield " ".join(words)


if __name__ == '__main__':
    for i in pick_combos("рэбрендинг но все стельки не очень"):
        print(i)
