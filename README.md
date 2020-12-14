# Tweet Thief
For all your Twitter monitoring needs. This repo leverages nitter.net, a lightweight JS-free 
alternative to Twitter, which is easily scrapable.

## Installation
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
There are two ways to main usages to this repo. The first:
```
$ python main.py <twitter_handle>
```
is a simple retrieval of the 5 most recent tweets for the given `twitter_handle` and then 
periodically checks for new ones every 10 minutes.

The second is a provided [Dockerfile](Dockerfile) which, when built, exposes a basic Flask API. At
this point, the Flask API does not run alongside the previous usage, with 10 min periodic checks. 
Currently, the API retrieves all the recent tweets on the initial load of the `nitter` page. Tweets 
can be queried with:
```
curl 'localhost:<port_number>/tweets?handle=<twitter_handle>'
port_number = 5000 (default)
```
Which will return a JSON structure containing the tweets. Alternatively, the Flask app can be 
modified to serve on localhost directly, and then the above query can work the same.

## Further Development
Further development of this repo would combine the two usages above, leveraging threading, to run 
the incremental tweet checks every 10 mins, with the collected tweets.
 
Additionally, the Twitter handle would be passed into the combined solution, rather than as a URL 
query, with each tweet being sent to stdout as required.

## Comments

Unit tests would also be a nice addition given more time. 

Not clear whether other output was appropriate, so all has been suppressed 
