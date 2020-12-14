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
$ python main.py <handle>
```
is a simple retrieval of the 5 most recent tweets for the given `handle` and then 
periodically checks for new ones every 10 minutes.

The second is a provided [Dockerfile](Dockerfile) which, when built, exposes a basic Flask API and 
logs for recent and new tweets.
 ```
docker build -t tweet-thief .
docker run -p 5000:5000 --name tweet_thief tweet-thief <handle>
```
 
 The 5 most recent tweets are retrieved on initial load . At
this point, the Flask API does not run alongside the previous usage, with 10 min periodic checks. 
Currently, the application retrieves all the recent tweets on the initial load of the `nitter` page. Tweets 
can be queried with:
```
curl localhost:<port_number>
port_number = 5000 (default)
```
Which will return a JSON structure containing the tweets retrieved so far. Alternatively, the Flask app can be 
modified to serve on localhost directly, and then the above query can work the same. For some added
JSON niceness, I also recommend install `jq` and running:
```
curl localhost:<port_number> | jq
```

## Further Development
Unit tests would be a nice addition given more time. 

Not a lot of error handling at this point. Just relying on [nitter](nitter.net) to just be working 
for example. Would be good to add some meaningful error messages, etc. for when things go wrong.
## Comments
Not clear whether other stdout output was appropriate (i.e. from requests to the Flask server) 
was appropriate, so all has been suppressed to keep it neat and tidy.

Wasn't sure whether there was an expected stdout format. I decided that a timezone appropriate 
timestamp with just the plain text from the tweet would be sufficient.

Also wasn't sure whether the intention was to use the Twitter site directly. Or if something like 
[nitter](nitter.net) was okay. I was using Twitter initially, however they make active attempts to 
prevent scraping, etc. and the API is no longer usable without an account. Twitter detects 
JavaScript in the browser, and blocks the usage when it can't be found (i.e. from scraping). With 
some `user-agent` manipulation, I was able to leverage a legacy mobile support from Twitter that 
allows for no JS, however, interestingly enough, this service is being discontinued 15/12/2020, 
the same day this is meant to be completed! Whilst a headless browser with `selenium` or something 
could have been used, `nitter.net` is basically designed to circumvent this problem, so it proved 
to be the nicer solution.
