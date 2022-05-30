#!/usr/bin/env python

""" 'Harry Potter and Shit' bot """
import sqlite3
from os import getenv

from mastodon import Mastodon


class HarryPotter:
    def __init__(self):
        params = {key: getenv(key) for key in 'client_id', 'client_secret', 'access_token', 'api_base_url'}
        self.client = Mastodon(**params)
        self.db = getenv('db')

    def run(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        phrase = cur.execute("SELECT phrase FROM phrase WHERE posted = 0 ORDER BY toot_id LIMIT 1").fetchone()[0]
        self.client.status_post(phrase, visibility='unlisted')
        cur.execute(f"UPDATE phrase SET posted = 1 WHERE phrase = '{phrase}'")
        conn.commit()
        conn.close()


if __name__ == '__main__':
    HarryPotter().run()
