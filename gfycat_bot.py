import praw
import pprint
import urllib
import time
import gfycat.gfycat
import traceback
import time
from datetime import datetime

debug = False

def process_sub(reddit,subreddit_name):
	print("Now running on: " + subreddit_name)
	#may need to be adjusted for subreddits with more postings per minute
	submission_generator = reddit.get_subreddit(subreddit_name).get_new(limit=5)
	for submission in submission_generator:
		post_id = vars(submission)['id']
		#file for keeping track of already processed links
		processed_file = open("processed.txt")
		#TODO: dont keep post IDs on file forever, maybe only the last 50?	
		if post_id in processed_file.read():
			print(post_id + ": Already processed")
			processed_file.close()
			continue
		title = submission.title
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
				with open("processed.txt", "a") as processed:
					processed.write(post_id + "\n")
				print("Processed: " + title + "\nPermalink: " + permalink)
			except Exception as e:
				print(post_id + ": Error while uploading this post, skipping to the next post...")
				if debug:
					traceback.print_exc()
				continue
		else:
			print(post_id + ": is not a GIF")
			continue
		time.sleep(5)

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
	return 'Here is a blazing fast gfycat version! ' + gifv + '\n\n' + original_size + '\n\n' +  new_size + '\n\n' + bandwidth + '\n\n____________________\n\nI am a bot. If I am misbehaving, please [message /u/QAFY](http://www.reddit.com/message/compose/?to=skylarmmb)'

def mainloop():
	print("~~~~ gfy__bot ~~~~")
	try:
		user_agent = ("#YOUR USER AGENT HERE#")
		reddit = praw.Reddit(user_agent = user_agent)
		reddit.login('#BOT USERNAME#','#BOT PASSWORD#')
		subreddits = ['#PUT SUBREDDITS#','#IN THIS ARRAY#','#FOR EXAMPLE#','gifs']
		for sub in subreddits:
			process_sub(reddit,sub)
		print("Done!")
	except Exception as e:
		print("Error at the login level (check network connection and that reddit isn't down).")
		traceback.print_exc()
		
mainloop()

