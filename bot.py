# coding: utf-8

import sys
from os import environ
from twitterbot_utils import Twibot, get_maximum_tweets
from mgrep import process_line

__author__ = "@strizhechenko"

READER = Twibot(username=environ.get('reader_name'))
TEMPLATE = unicode(environ.get('template', u''), 'utf-8')


def get_tweets():
    return get_maximum_tweets(READER.api.home_timeline)


def print_tweets(tweets):
    for tweet in tweets:
        print tweet.encode('utf-8')


def read_tweets(filename):
    with open(filename) as f:
        return (unicode(tweet, 'utf-8') for tweet in f.readlines())


def do_tweets():
    """ периодические генерация и постинг твитов """
    # in case of using on non-twitter source of words:
    # tweets = read_tweets('file-with-words-path')
    tweets = get_tweets()
    for tweet in tweets:
        result = process_line(tweet)
        if result:
            print u"Гарри Поттер и {0}".format(result).encode('utf-8')


if __name__ == '__main__':
    do_tweets()
