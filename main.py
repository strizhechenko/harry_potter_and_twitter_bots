#!/usr/bin/env python3
""" Гарри Поттер и Парсинг lor.sh """
# coding: utf-8

import argparse
import logging
import sqlite3

import html2text
import requests
from mgrep import pick_combos

h = html2text.HTML2Text()
h.ignore_links = h.ignore_images = True
logging.basicConfig(level=logging.WARNING)


def parse_args():
    """ Разбор аргументов"""
    parser = argparse.ArgumentParser()
    parser.description = "Вытянуть последние N записей из мастодон в свой SQLite для фразочек бота"
    parser.add_argument('--url', default='https://lor.sh/api/v1/timelines/public?local=true', type=str, help='API URL')
    parser.add_argument('--db', default='harry_potter_and_twitter_bots/mbot.sqlite', type=str, help='Cache DB')
    parser.add_argument('--init', action='store_true', help="Создать БД")
    parser.add_argument('--limit', default=40, type=int, help='Limit')
    args = parser.parse_args()
    args.url = f'{args.url}&limit={args.limit}'
    return args


def toots2toots(cur):
    for _id, content in cur.execute("SELECT id, content FROM toot WHERE processed = 0 ORDER BY id DESC").fetchall():
        for combo in pick_combos(content):
            count = cur.execute(f"SELECT count(1) FROM phrase WHERE phrase='{combo}'").fetchone()[0]
            if count == 0:
                # toot_id нужен для отладки, чтобы понимать откуда фраза взялась
                cur.execute(f"INSERT INTO phrase (toot_id, phrase) VALUES ({_id}, '{combo}')")
                print(f"Гарри Поттер и {combo}")
        cur.execute(f"UPDATE toot SET processed = 1 where id = {_id}")


def update_toots(url, cur, html):
    max_id = cur.execute("SELECT max(id) FROM toot").fetchone()[0]
    if max_id:
        url = f'{url}&since_id={max_id}'
    data = requests.get(url).json()
    logging.debug("Fetched %d items", len(data))
    for toot in data:
        content = html.handle(toot.get('content')).replace("'", "").strip()
        if not content:
            continue
        count = cur.execute(f"SELECT count(1) FROM toot WHERE id={toot.get('id')}").fetchone()[0]
        if count == 0:
            sql = f"INSERT INTO toot (id, content) VALUES ({toot.get('id')}, '{content}')"
            cur.execute(sql)


def init(cur):
    cur.execute("""create table phrase
        (
            phrase  text not null constraint phrase_pk primary key,
            posted  int default 0 not null,
            toot_id int
        );""")
    cur.execute("create unique index phrase_phrase_uindex on phrase (phrase);")
    cur.execute("""
        create table toot
        (
            id        int  not null
                constraint toot_pk
                    primary key,
            content   text not null,
            processed int default 0 not null
        );""")
    cur.execute("create unique index toot_id_uindex on toot (id);")


def main():
    args = parse_args()
    html = html2text.HTML2Text()
    html.ignore_links = html.ignore_images = True
    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    if args.init:
        init(cur)
    update_toots(args.url, cur, html)
    toots2toots(cur)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
