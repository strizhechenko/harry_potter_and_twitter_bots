# coding: utf-8

from os import environ
from twitterbot_utils import Twibot, get_maximum_tweets
from mgrep import process_line

__author__ = "@strizhechenko"

TEMPLATE = unicode(environ.get('template', u''), 'utf-8')


def read_tweets(filename):
    with open(filename) as f:
        return (unicode(tweet, 'utf-8') for tweet in f.readlines())


def main():
    # in case of using on non-twitter source of words:
    # tweets = read_tweets('file-with-words-path')
    reader = Twibot(username=environ.get('reader_name'))
    tweets = get_maximum_tweets(reader.api.home_timeline)
    for tweet in tweets:
        result = process_line(tweet)
        if result:
            print TEMPLATE.format(result).encode('utf-8')


if __name__ == '__main__':
    main()
