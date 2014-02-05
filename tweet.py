#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser, os, subprocess, re, tweepy

def get_fortune():
    fortune = subprocess.Popen(['fortune'], stdout=subprocess.PIPE)
    fortune = fortune.communicate()[0]

    fortune = re.sub(r"[\n|\r]", ' ', fortune)
    fortune = re.sub(r"\s{1,}", ' ', fortune)
    fortune = fortune.strip()

    if len(fortune) > 140:
        return get_fortune()

    return fortune

def get_api_client():
    config = ConfigParser.ConfigParser()
    ini = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')

    config.read(ini)

    consumer_key = config.get('Consumer', 'key')
    consumer_secret = config.get('Consumer', 'secret')

    access_key = config.get('Access', 'key')
    access_secret = config.get('Access', 'secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return tweepy.API(auth)

def tweet_fortune():
    api_client = get_api_client()
    fortune = get_fortune()

    api_client.update_status(fortune)

tweet_fortune()
