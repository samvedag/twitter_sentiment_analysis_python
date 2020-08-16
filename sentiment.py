import re 
import tweepy 
import nltk
from tweepy import OAuthHandler 
from textblob import TextBlob 
import numpy as np

class TwitterClient(object): 
	
	def __init__(self): 
		# initialization method. 
		# keys and tokens from the dev.twitter.com Twitter App
		API_key = 'XXXXXX'
		API_secret = 'XXXXXXX'
		access_token = 'XXXXXXX'
		access_token_secret = 'XXXXXX'
		# insert all the keys and tokens above after generating them newly everytime

		# attempt at authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(API_key, API_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		# using regex substitution to clean tweet text by removing links and special characters 
	
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|( *RT*)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet): 
		# differentiating tweets into categories
		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 4): 
		# Main function to fetch tweets and parse them. 
		tweets = [] 
		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets 
			for tweet in fetched_tweets: 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending tweets
				if tweet.retweet_count > 0: 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 			
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	print("Enter your query precisely - ")
	twitter_query = input()
	tweets = api.get_tweets(query = twitter_query, count = 200) 
	# picking positive tweets from tweets 
	positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets 
	print("Positive tweets percentage: {}%".format(100*len(positive_tweets)/len(tweets)))
	# picking negative tweets from tweets 
	negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets 
	print("Negative tweets percentage: {}%".format(100*len(negative_tweets)/len(tweets)))
	# picking neutral tweets from tweets
	neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {}% \n".format(100*(len(tweets) -(len( negative_tweets )+len( positive_tweets)))/len(tweets))) 

	# printing positive tweets 
	print("\n\nPositive tweets:") 
	for tweet in positive_tweets[:2]: 
		print(tweet['text']) 

	# printing negative tweets 
	print("\n\nNegative tweets:") 
	for tweet in negative_tweets[:2]: 
		print(tweet['text']) 

        # printing neutral tweets
	print("\n\nNeutral tweets:")
	for tweet in neutral_tweets[:2]:
		print(tweet['text'])


if __name__ == "__main__": 
	main() 
