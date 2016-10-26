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
        print self.connection['__last_tweet_id__'], len(text_input)
        text_input = dict(self.unprocessed_lines())
        for key in sorted(text_input, key=int):
            result = process_line(unicode(text_input[str(key)], 'utf-8'))
            if not result or self.connection.get(result):
                print 'skip', result
                continue
            tweet = unicode(self.template, 'utf-8').format(result).encode('utf-8')
            try:
                tweet_rc = self.twibot.api.update_status(tweet)
                # pylint: disable=E1101
                self.connection[result] = tweet_rc.id
                self.connection['__last_tweet_id__'] = key
                print 'ok', key, tweet
                break
            except TweepError:
                self.connection['__last_tweet_id__'] = key
                print 'fail', key, tweet

if __name__ == '__main__':
    HarryPotter(getenv('username'), getenv('host', '127.0.0.1')).run()
