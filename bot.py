#!/usr/bin/env python

""" 'Harry Potter and Shit' bot """
from os import getenv
from twitterbot_farm import Writer
from mgrep import process_line
from tweepy.error import TweepError


class HarryPotter(Writer):

    def __init__(self, username, host='127.0.0.1'):
        Writer.__init__(self, username, host)

    def run(self):
        self.connection['__last_tweet_id__'] = self.connection.get('__last_tweet_id__', '1')
        text_input = dict(self.unprocessed_lines())
        for key in sorted(text_input, key=int):
            result = process_line(unicode(text_input[str(key)], 'utf-8'))
            if not result or self.connection.get(result):
                continue
            try:
                self.tweet(key, result)
                break
            except TweepError:
                self.connection['__last_tweet_id__'] = key


if __name__ == '__main__':
    HarryPotter(getenv('username'), getenv('host', '127.0.0.1')).run()
