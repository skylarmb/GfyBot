import praw
import pprint
import urllib
import time
import gfycat.gfycat

user_agent = ("##YOUR DESIRED BOT USER AGENT##")
reddit = praw.Reddit(user_agent = user_agent)
reddit.login('##YOUR REDDIT BOT USERNAME##','##YOUR REDDIT BOT PASSWORD##')
v_fixed = []

submission_generator = reddit.get_subreddit('gfy__bot__test').get_new(limit=5)

found_something = False

for submission in submission_generator:
	post_id = vars(submission)['id']
	if post_id in open("processed.txt").read():
		print("Already processed")
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
			#print("gifv version: " + gifv)
			v_fixed.append([url,gifv])
			submission.add_comment('Here is a blazing fast gfycat version! ' + gifv)
			print("Title: " + title + "\nPermalink: " + permalink + "\nURL: " + url + "\ngifv: " + gifv)
			with open("processed.txt", "a") as test:
				test.write(post_id + "\n")
		except:
			print("Looks like an error, skipping to the next post...")
			continue
	time.sleep(5)