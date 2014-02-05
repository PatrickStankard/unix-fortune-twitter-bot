#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import sub
from os import path
from sys import exit
from tweepy import OAuthHandler, API
from subprocess import Popen, PIPE
from ConfigParser import ConfigParser

def get_config():
    config = ConfigParser()
    ini = path.join(path.abspath(path.dirname(__file__)), 'config.ini')

    config.read(ini)

    return config

def get_api_client():
    config = get_config()

    consumer_key = config.get('Consumer', 'key')
    consumer_secret = config.get('Consumer', 'secret')
    access_key = config.get('Access', 'key')
    access_secret = config.get('Access', 'secret')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return API(auth)

def get_fortune(retry_count=0, tweets=[]):
    cmd = Popen(['fortune'], stdout=PIPE, stderr=PIPE)
    out, err = cmd.communicate()

    if out:
        out = sub(r"[\n|\r]", ' ', out)
        out = sub(r"\s{1,}", ' ', out)
        out = out.strip()

        if len(out) > 140:
            return retry_fortune(retry_count, tweets)

        for tweet in tweets:
            if tweet.text == out:
                return retry_fortune(retry_count, tweets)

        return out
    if err:
        return retry_fortune(retry_count, tweets)

def retry_fortune(retry_count=0, tweets=[]):
    retry_count += 1

    if retry_count > 225:
        exit(1)

    return get_fortune(retry_count, tweets)

def tweet_fortune():
    api_client = get_api_client()
    tweets = api_client.user_timeline(count=200)

    fortune = get_fortune(0, tweets)

    api_client.update_status(fortune)

tweet_fortune()
