#!/usr/bin/env python

# coding: utf-8

# pylint: disable=C0111,C0103

from os import getenv
from twitterbot_utils import Twibot, get_maximum_tweets
from dictator import Dictator
from mgrep import process_line

__author__ = "@strizhechenko"

TEMPLATE = unicode(getenv('template', u''), 'utf-8')


class Tweets(object):

    def __init__(self, source='net', filename='tweets.txt', net_count=100, redis_db=1):
        self.reader = None
        self.tweets = []
        self.filename = filename

        if source == 'local':
            self.read()
            return

        if source == 'redis':
            self.redis = dictator(redis_db)
            return

        if source == 'net':
            self.reader = Twibot(username=getenv('reader_name'))
            if net_count >= 200:
                self.net_max()
            else:
                self.net(net_count)

    def write(self):
        tweets = [t.text.encode('utf-8') for t in self.tweets]
        with open(self.filename, 'w') as f:
            tweets.append('')
            f.write("\n".join(tweets))

    def read(self):
        with open(self.filename) as f:
            self.tweets = (unicode(tweet, 'utf-8') for tweet in f.readlines())

    def net(self, count):
        self.tweets = [t.text for t in self.reader.api.home_timeline(count=count)]

    def net_max(self):
        self.tweets = get_maximum_tweets(self.reader.api.home_timeline, logging=True)

    def process(self):
        for tweet in self.tweets:
            result = process_line(tweet)
            if result:
                print TEMPLATE.format(result).encode('utf-8')


if __name__ == '__main__':
    Tweets('net', net_count=1000).process()
