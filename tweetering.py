""" Streaming twitter API example """


from __future__ import print_function
import sys
import tweepy
from configparser import ConfigParser
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <word>" % (sys.argv[0]))
        sys.exit()
    query = sys.argv[1]
    print("Listening to " + query )
    print("Tweets are written on "+query+".txt")
    print("Press CTRL + c to terminate...")
    time.sleep(2)

    config = ConfigParser()
    # read configuration
    config.read('config.cfg')


    auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'),
                               config.get('twitter', 'consumer_secret'))

    auth.set_access_token(config.get('twitter', 'access_token'),
                          config.get('twitter', 'access_token_secret'))

    api = tweepy.API(auth) # create a twitter client
    i = 1
    max_tweets = 100
    searched_tweets = []
    last_id = -1
    file = open(query + '.txt', mode='w', encoding='utf-8')
    while True:
        try:
            count = max_tweets - len(searched_tweets)
            new_tweets = api.search(q=query, tweet_mode='extended', lang='en', count=count, max_id=str(last_id - 1))
            to_write = ''
            if not new_tweets:
                break
            for tweet in new_tweets:
                if 'retweeted_status' in tweet._json:
                    to_write += 'RT @ ' + tweet._json['retweeted_status']['full_text'].replace('\n', ' ') + '\n'
                else:
                    to_write += tweet.full_text.replace('\n', ' ') + '\n'
                i += 1
            file.write(to_write)
            print(to_write)
        except KeyboardInterrupt:
            print('*****************************\nInterrupted')
            file.close()
            sys.exit()
