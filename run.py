import argparse
import logging
import os

from flask import Flask
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

from main import get_new_tweets, print_tweets

app = Flask(__name__)


def tweet_listener(event):
    print_tweets(event.retval)
    TWEET_LIST.extend(event.retval)


@app.route("/")
def api():
    return {
        "tweets": [{
            'body': tweet['body'],
            'time': tweet['time']
        } for tweet in TWEET_LIST]
    }


if __name__ == '__main__':
    # Handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('handle', help='Twitter handle to monitor')
    args = parser.parse_args()

    # Suppress all Flask related logging
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    TWEET_LIST = []

    # Create and configure scheduler to check for and update tweets every 10 minutes
    scheduler = BackgroundScheduler(job_defaults=dict(max_instances=1))
    scheduler.add_job(get_new_tweets, 'interval', minutes=10, args=(TWEET_LIST, args.handle))
    scheduler.add_listener(tweet_listener, EVENT_JOB_EXECUTED)

    # Only want first 5 tweets initially
    initial_tweets = get_new_tweets([], handle=args.handle, limit=5)
    print_tweets(initial_tweets)
    TWEET_LIST.extend(initial_tweets)

    scheduler.start()
    app.run(host='0.0.0.0', use_reloader=False)
