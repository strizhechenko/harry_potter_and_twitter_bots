import logging
from unittest import TestCase

from harry_potter_and_twitter_bots.mgrep import pick_combos


class TestMgrep(TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")

    def _check_it(self, line, expected):
        self.assertEqual(expected, list(pick_combos(line)))

    def test_it(self):
        self._check_it("своих старых", [])
        self._check_it("просто набор", [])
        self._check_it("гадкий я", [])
        self._check_it("по крайней мере", ["Крайняя Мера"])
        self._check_it("достаточно длинная строка для проверки итерации", ["Длинная Строка"])
        self._check_it("неправильные схемы", ["Неправильные Схемы"])
        self._check_it("согласованных словосочетаний", ["Согласованные Словосочетания"])
