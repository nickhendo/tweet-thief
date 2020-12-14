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
    tweets, _ = update_tweets([], timeline)
    return {
        "tweets": [{
            'body': tweet['body'],
            'time': tweet['time']
        } for tweet in tweets]
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
