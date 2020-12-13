from flask import Flask
from flask import request

from main import get_timeline, update_tweets

app = Flask(__name__)


@app.route("/tweets")
def api():
    handle = request.args.get('handle')
    if not handle:
        return {}
    timeline = get_timeline(handle)
    tweets = update_tweets([], timeline)
    return {
        "tweets": [{
            'body': tweet['body'],
            'time': tweet['time']
        } for tweet in tweets]
    }

