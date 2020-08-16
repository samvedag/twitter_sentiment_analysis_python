import re 
import tweepy 
import nltk
from tweepy import OAuthHandler 
from textblob import TextBlob 
import numpy as np

class TwitterClient(object): 
	
	def __init__(self): 
		# class constructor or initialization method. 
		# keys and tokens from the Twitter Dev Console 
		API_key = 'Nxcfrc4iNURCjJbkfbKM5g8bB'
		API_secret = 'Gd4LTQQU6ZMwTrQizwK2gHDXUHBEbcO399B58PpZ520oI2Et6g'
		access_token = '1294716282948861952-wVYjKZJ7WPNdme06NhWQ8t39zENILF'
		access_token_secret = 'OdHK0j6P8qzvCd3G821wEpcEcFwzWe6T05n5CX72gqjsN'

		# attempt authentication 
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
		# using regex to clean tweet text by removing links, special characters 
	
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|( *RT*)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet): 
		# function to check the sentiment, that is the polarity of the tweet
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 4): 
		
		# Main function to fetch tweets and parse them. 
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	print("Enter your query precisely - ")
	twitter_query = input()
	tweets = api.get_tweets(query = twitter_query, count = 200) 
	# cleaning tweets

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


	print("\n\nNeutral tweets:")
	for tweet in neutral_tweets[:2]:
		print(tweet['text'])


if __name__ == "__main__": 
	# calling main function 
	main() 
