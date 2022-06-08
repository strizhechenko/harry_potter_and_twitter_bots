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


def morph(parsed: list, grammems: set, forms: set) -> str or None:
    """
    Ищем в распарсенном слове наиболее подходящий под все требования вариант:
    :param parsed: анализруемое слово парсится в список наиболее вероятных результатов парсинга
    :param grammems: множество граммем: падеж, число и опционально пол.
    :param forms : обычно просто часть речи (существительное/прилагательное/причастие), но для причастия нужен залог.
        Это множество используется дважды:
        1. При отбросе неправильных вариантов парсинга слова
        2. При выборе подходящей по всем параметрам лексемы.
    :return: либо _идеальное_ слово с большой буквы, либо ничего.
    """
    for word in parsed:
        if all(form in word.tag for form in forms) and word.score > 0.1:  # < 0.1 - высосано из пальца.
            for lexeme in word.lexeme:
                if lexeme.normal_form in IGNORE_WORDS:
                    return
                if 'Name' not in lexeme.tag:
                    if all(grammem in lexeme.tag for grammem in grammems | forms):
                        return lexeme.word.capitalize()


def add_common_tag(words: list, category: tuple, tags: set) -> bool or None:
    """
    Ищем общий тег в заданной категории (множестве тегов) в двух словах.
    :param words: собственно, распарсенные слова.
    :param category: множество допустимых общих тегов (ТОТ САМЫЙ СПИСОК ВСЕХ ГЕНДЕРОВ)
    :param tags: итоговое множество общих тегов, которое затем будет использовано для фильтрации вариантов слов.
    :return: True, если тег нашёлся и добавлен в множество общих тегов, None если нет. Эдакий int rc.
    """
    for tag in category:
        if all(any(tag in w.tag for w in word) for word in words):
            tags.add(tag)
            return True


def detect_adjf_tags(adjf):
    """ Причастие (PRTF) должно сохранять свой изначальный залог (Adjx), иначе морфер может сильно исказить смысл """
    adjf_tags = {'ADJF'}
    if 'PRTF' in adjf[0].tag:
        adjf_tags = {'PRTF'}
        if 'Adjx' in adjf[0].tag:
            adjf_tags.add('Adjx')
    return adjf_tags


def morphs(words: tuple) -> tuple:
    """
    :param words: входящая пара слов (2 строки)
    :return: исходящая пара слов (2 строки или None, None)
    """
    parsed = list(map(morpher.parse, words))
    common_tags = {'nomn'}  # стараемся привести всё к именительному падежу
    # Обеспечиваем согласованность по числу, множественное в приоритете
    if not add_common_tag(parsed, ('plur', 'sing'), common_tags):
        return None, None  # нужно для работы all(result := )
    if 'sing' in common_tags:  # И, в случае единственного числа, по полу
        add_common_tag(parsed, ('masc', 'femn', 'neut'), common_tags)
    logging.debug("common_tags %s", common_tags)
    adjf, nomn = parsed
    adjf_tags = detect_adjf_tags(adjf)
    adjf = morph(adjf, common_tags, adjf_tags)
    if not adjf:  # ради того чтобы морфер не потел с существительным, если уже ясно что ничего не вышло
        return None, None
    return adjf, morph(parsed[1], common_tags, {'NOUN'})


def pick_combos(line: str):
    """
    Точка входа в библиотеку.
    :param line: просто строка текста. Хоть целую книгу можно сюда засунуть.
    :return: подходящие под заданный шаблон пары слов
    """
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
