import tweepy
import os

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler("TWITTER_API_KEY", "TWITTER_API_KEY_SECRET")
auth.set_access_token("TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET")


# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)


timeline = api.home_timeline()
for tweet in timeline:
    print(f"{tweet.user.name} said {tweet.text}")

# Create a tweet
#api.update_status("Hello Pvrple Bot Test three by Tweepy")

user = api.get_user("MikezGarcia")

print("User details:")
print(user.name)
print(user.description)
print(user.location)

print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)


#api.create_friendship("pvrple_blvck_sa")
api.update_profile(description="I AM Pvrple Blvck.by TweepyBot")

#Like most recent tweet
'''tweets = api.home_timeline(count=1)
tweet = tweets[0]
print(f"Liking tweet {tweet.id} of {tweet.author.name}")
api.create_favorite(tweet.id)'''


#See blocked contacts
for block in api.blocks():
    print(block.name)


#Search Tweets
for tweet in api.search(q="Bitcoin", lang="en", rpp=10):
    print(f"{tweet.user.name}:{tweet.text}")


#Trends 
trends_result = api.trends_place(1)
for trend in trends_result[0]["trends"]:
    print(trend["name"])

