debug = False
#the message/disclaimer that is printed at the bottom of each comment
usermessage = 'Something here'
app_key = 'YourAppKeyHere'
app_secret = 'YourAppSecretHere'
refresh_token = 'YourRefreshTokenHere'
access_token = 'YourAccessTokenHere'
#permissions for the bot. these defaults should be fine
scopes = ['identity', 'read', 'submit']
#subreddits to run on
subreddits = ['subreddits','here']
#path to processed file. If using crontab for scheduling, this should be absolute
processed_file = '/path/to/processed.txt'
#Your unique identifier
user_agent = "your_user_agent_here"
#time to sleep between submissions (to avoid busting the rate limit)
sleep_time = 5
#number of posts to fetch from each sub at runtime
number_of_posts = 5