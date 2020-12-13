import argparse
import pytz
import requests
import sys
import time

from bs4 import BeautifulSoup
from datetime import datetime
from tzlocal import get_localzone


REFRESH_TIME = 5


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


def update_tweets(current_list, timeline):
    tweet_timezone = pytz.timezone('UTC')
    local_timezone = get_localzone()
    for tweet in timeline:
        # Tweet times are returned as UTC, this converts to the local system timezone
        tweet_time = tweet_timezone.localize(
                datetime.strptime(tweet.find('span', 'tweet-date').a['title'],
                                  '%d/%m/%Y, %H:%M:%S')).astimezone(local_timezone)
        tweet_body = tweet.find('div', 'tweet-content').text
        if all(tweet_time > tweet['time'] for tweet in current_list):
            current_list.append({
                'body': tweet_body,
                'time': tweet_time,
                'printed': False
            })
    return current_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('handle', help='Twitter handle to monitor')
    args = parser.parse_args()
    twitter_handle = args.handle

    timeline = get_timeline(twitter_handle)
    tweet_list = update_tweets([], timeline)

    # Only interested in the 5 most recent tweets
    del tweet_list[:-5]

    for tweet in tweet_list:
        print(tweet['time'].ctime())
        print(f"{tweet['body']}\n")
        tweet['printed'] = True

    while True:
        timeline = get_timeline(twitter_handle)
        tweet_list = update_tweets(tweet_list, timeline)
        for tweet in [t for t in tweet_list if not t['printed']]:
            print(tweet['time'].ctime(), tweet['body'])
            tweet['printed'] = True
        time.sleep(REFRESH_TIME)


if __name__ == '__main__':
    main()
