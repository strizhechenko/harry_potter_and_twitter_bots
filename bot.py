#!/usr/bin/env python

from os import getenv
from twitterbot_farm import Writer
from mgrep import process_line


class HarryPotter(Writer):

    def __init__(self, username, host='127.0.0.1'):
        Writer.__init__(self, username, host)

    def run(self):
        self.connection['__last_tweet_id__'] = 1
        for key, text in self.unprocessed_lines():
            result = process_line(unicode(text, 'utf-8'))
            if result:
                tweet = unicode(self.template, 'utf-8').format(result).encode('utf-8')
                print key, tweet
                self.twibot.api.update_status(tweet)
                self.connection['__last_tweet_id__'] = key

if __name__ == '__main__':
    HarryPotter(getenv('username'), getenv('host', '127.0.0.1')).run()
