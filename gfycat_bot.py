import praw
import pprint
import urllib
import time
import gfycat.gfycat
import traceback
import time
from datetime import datetime
from prawoauth2 import PrawOAuth2Mini
import settings as s

nothing_to_do = True
debug = s.debug

#Set up global reddit auth
reddit = praw.Reddit(user_agent = s.user_agent)
oauth_helper = PrawOAuth2Mini(reddit, app_key=s.app_key,
                      app_secret=s.app_secret,
                      access_token=s.access_token,
                      refresh_token=s.refresh_token, scopes=s.scopes)

def process_sub(reddit,subreddit_name):
	global nothing_to_do
	if debug:
		print("Now running on: " + subreddit_name)
	#number_of_posts needs to be adjusted for subreddits with more postings per minute. Do so in settings.py
	submission_generator = reddit.get_subreddit(subreddit_name).get_new(limit=s.number_of_posts)
	for submission in submission_generator:
		post_id = vars(submission)['id']
		#file for keeping track of already processed links. Set in settings.py
		processed_file = open(s.processed_file)
		#TODO: dont keep post IDs on file forever, maybe only the last 50?	
		if post_id in processed_file.read():
			if debug:
				print(post_id + ": Already processed")
			processed_file.close()
			continue
		url = vars(submission)['url']
		permalink = vars(submission)['permalink']
		if debug:
			print(pprint.pprint(vars(submission)))
		extension = url[len(url)-3:]
		#if the post is a gif, lets process it
		if(extension == "gif"):
			try:
				#weird, but it works
				upload = gfycat.gfycat.gfycat().upload(url)
				submission.add_comment(create_comment(upload))
				#successfully processed post, add ID to file
				with open(s.processed_file, "a") as processed:
					processed.write(post_id + "\n")
				print(prefix() + "Processed: " + post_id + " on " + subreddit_name)
				nothing_to_do = False
			except Exception as e:
				print(prefix() + post_id + ": Error, skipping...")
				if debug:
					traceback.print_exc()
				continue
		else:
			if debug:
				print(post_id + ": is not a GIF")
			continue
		time.sleep(s.sleep_time)

def create_comment(upload):
	if debug:
		print(upload.formated()) 
	gifv = "http://gfycat.com/" + upload.get("gfyName")
	gif_size_formatted = upload.get("gifSize") / 1000000.0
	gfy_size_formatted = upload.get("gfysize") / 1000000.0
	original_size = ""
	new_size = ""
	bandwidth = ""
	if(gif_size_formatted >= 1):
		original_size = ("Original size: %.2fmb" % gif_size_formatted)
	else:
		original_size = ("Original size: %dkb" % (gif_size_formatted*1000))
	if(gfy_size_formatted >= 1):
		new_size = ("New size: %.2fmb" % gfy_size_formatted)
	else:
		new_size = ("New size: %dkb" % (gfy_size_formatted*1000))
	if((gif_size_formatted - gfy_size_formatted) < 1):
		bandwidth = ("Bandwidth saved: %dkb" % (gif_size_formatted*1000 - gfy_size_formatted*1000))
	else:
		bandwidth = ("Bandwidth saved: %.2fmb" % (gif_size_formatted - gfy_size_formatted))
	return 'Here is a blazing fast gfycat version! ' + gifv + '\n\n' + original_size + '\n\n' +  new_size + '\n\n' + bandwidth + '\n\n____________________\n\n' + s.usermessage

def prefix():
	return str(datetime.now()).split(".")[0] + " | "

def mainloop():
	global nothing_to_do
	nothing_to_do = True
	try:
		subreddits = s.subreddits
		for sub in subreddits:
			process_sub(reddit,sub)
		if(nothing_to_do):
			print(prefix() + "Nothing to do")
		else:
			print(prefix() + "Completed successfully")
	except praw.errors.OAuthInvalidToken:
		print(prefix() + "Error at the login level, refreshing tokens.")
		print()
		oauth_helper.refresh()
		mainloop()
		
mainloop()

