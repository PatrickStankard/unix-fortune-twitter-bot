#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from os import path
from subprocess import Popen, PIPE
from re import sub
from tweepy import OAuthHandler, API
from sys import exit

def get_fortune(retry_count=0):
    cmd = Popen(['fortune'], stdout=PIPE, stderr=PIPE)
    out, err = cmd.communicate()

    if out:
        out = sub(r"[\n|\r]", ' ', out)
        out = sub(r"\s{1,}", ' ', out)
        out = out.strip()

        if len(out) > 140:
            return retry_fortune(retry_count)

        return out
    if err:
        return retry_fortune(retry_count)

def retry_fortune(retry_count=0):
    retry_count += 1

    if retry_count > 10:
        exit(1)

    return get_fortune(retry_count)

def get_api_client():
    config = ConfigParser()
    ini = path.join(path.abspath(path.dirname(__file__)), 'config.ini')

    config.read(ini)

    consumer_key = config.get('Consumer', 'key')
    consumer_secret = config.get('Consumer', 'secret')

    access_key = config.get('Access', 'key')
    access_secret = config.get('Access', 'secret')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return API(auth)

def tweet_fortune():
    api_client = get_api_client()
    fortune = get_fortune()

    api_client.update_status(fortune)

tweet_fortune()
