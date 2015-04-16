import praw
import pprint
import urllib
import time
import gfycat.gfycat
import traceback
import time
from datetime import datetime

def do_the_thing(v_fixed,reddit,subreddit_name):
	print("~~~ Now running on: " + subreddit_name + " ~~~")
	submission_generator = reddit.get_subreddit(subreddit_name).get_new(limit=5)

	found_something = False

	for submission in submission_generator:
		post_id = vars(submission)['id']
		processed_file = open("processed.txt")	
		if post_id in processed_file.read():
			print("Already processed")
			processed_file.close()
			continue
		title = submission.title
		found_something = True
		url = vars(submission)['url']
		permalink = vars(submission)['permalink']
		#print(pprint.pprint(vars(submission)))
		extension = url[len(url)-3:]
		if(extension == "gif"):
			try:
				upload = gfycat.gfycat.gfycat().upload(url)
				gifv = "http://gfycat.com/" + upload.get("gfyName")
				gif_size = upload.get("gifSize")
				gfy_size = upload.get("gfysize")
				gif_size_formatted = (gif_size / 1000000.0)
				gfy_size_formatted = (gfy_size / 1000000.0)
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
					
				#print(upload.formated())
				v_fixed.append([url,gifv])
				submission.add_comment('Here is a blazing fast gfycat version! ' + gifv + '\n\n' + original_size + '\n\n' +  new_size + '\n\n' + bandwidth + '\n\n____________________\n\nI am a bot. If I am misbehaving, please [message /u/skylarmmb](http://www.reddit.com/message/compose/?to=skylarmmb)')
				print("Processed: " + title + "\nPermalink: " + permalink)
				with open("processed.txt", "a") as test:
						test.write(post_id + "\n")
			except Exception as e:
				print("Looks like an error with this post, skipping to the next post...")
				traceback.print_exc()
				continue
		time.sleep(5)
def mainloop():
	while(True):
		print(str(datetime.now()))
		try:
			user_agent = ("gfy_mirror_bot")
			reddit = praw.Reddit(user_agent = user_agent)
			reddit.login('gfy__bot','gfybotpassword')
			v_fixed = []
			subreddit_names = ['gfy__bot__test','cutegirlgifs']
			for name in subreddit_names:
				do_the_thing(v_fixed,reddit,name)
			print("Done! Resting for 5 minutes")
			time.sleep(300)
		except Exception as e:
			print("Error at the login level, waiting 1 minute to try again")
			traceback.print_exc()
			time.sleep(60)
			continue
		
mainloop()
