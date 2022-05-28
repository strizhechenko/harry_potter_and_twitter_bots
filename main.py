#!/usr/bin/env python
""" TODO: опишите, что это за скрипт """
# coding: utf-8

import argparse
import sqlite3
import html2text
import requests

from harry_potter_and_twitter_bots.mgrep import pick_combos

h = html2text.HTML2Text()
h.ignore_links = h.ignore_images = True


def parse_args():
    """ Разбор аргументов"""
    parser = argparse.ArgumentParser()
    parser.description = "Опишите, что делает утилита"
    parser.add_argument('--url', default='https://lor.sh/api/v1/timelines/public?local=true', type=str, help='API URL')
    parser.add_argument('--limit', default=20, type=int, help='Limit')
    args = parser.parse_args()
    args.url = f'{args.url}&limit={args.limit}'
    return args


def main():
    args = parse_args()
    html = html2text.HTML2Text()
    html.ignore_links = html.ignore_images = True
    for toot in requests.get(args.url).json():
        import json; print(json.dumps(toot, indent=2, ensure_ascii=False)); exit(1)
        for combo in pick_combos(html.handle(toot.get('content'))):
            print(f"Гарри Поттер и {combo}")


if __name__ == '__main__':
    main()
