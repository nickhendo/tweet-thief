import argparse
import pytz
import requests
import sys
import time

from bs4 import BeautifulSoup
from datetime import datetime
from tzlocal import get_localzone


def get_timeline(twitter_handle):
    # Nitter is used as Twitter has JavaScript detection, which complicates web scraping. The API
    # is no longer accessible without auth. A legacy supported non-JS requiring mobile version of
    # Twitter does still exist which can be scraped, however will be taken down 15/12/2020
    nitter_url = f'https://nitter.net/{twitter_handle}'
    html = requests.get(nitter_url)
    soup = BeautifulSoup(html.content, 'html.parser')
    # Capture errors related to not being able to find a user, etc
    if soup.find('div', 'error-panel'):
        error_text = soup.find('div', 'error-panel').find('span').text
        print(error_text)
        sys.exit(1)
    timeline = soup.find_all('div', 'timeline-item')
    # Tweets are most recent at top of HTML but want them most recent at bottom of stdout
    timeline.reverse()
    return timeline


def get_raw_tweets(current_list, timeline):
    new_tweets = []
    tweet_timezone = pytz.timezone('UTC')
    local_timezone = get_localzone()
    for tweet in timeline:
        # Tweet times are returned as UTC, this converts to the local system timezone
        tweet_time = tweet_timezone.localize(
                datetime.strptime(tweet.find('span', 'tweet-date').a['title'],
                                  '%d/%m/%Y, %H:%M:%S')).astimezone(local_timezone)
        tweet_body = tweet.find('div', 'tweet-content').text
        if all(tweet_time > tweet['time'] for tweet in current_list):
            tweet_dict = {
                'body': tweet_body,
                'time': tweet_time,
            }
            new_tweets.append(tweet_dict)
    return new_tweets


def print_tweets(tweets):
    for tweet in tweets:
        print(f"{tweet['time'].ctime()}: {tweet['body']}")


def get_new_tweets(current_tweets, handle, limit=None):
    timeline = get_timeline(handle)
    tweet_list = get_raw_tweets(current_tweets, timeline)
    if limit:
        # Only interested in the 5 most recent tweets
        del tweet_list[:-limit]
    return tweet_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('handle', help='Twitter handle to monitor')
    args = parser.parse_args()
    # Only want first 5 initially
    tweet_list = get_new_tweets([], args.handle, limit=5)
    print_tweets(tweet_list)
    while True:
        new_tweets = get_new_tweets(tweet_list, args.handle)
        print_tweets(new_tweets)
        tweet_list.extend(new_tweets)
        time.sleep(600)
