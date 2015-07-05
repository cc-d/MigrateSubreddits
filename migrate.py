#!/usr/bin/env python
import json
import praw

def main():
	with open('config.json', 'r') as c:
		config = json.loads(c.read())

	print 'Retrieving list of subreddits.'
	r = praw.Reddit(config['user-agent'])
	r.login(config['from']['user'], config['from']['passwd'])
	subreddits = r.get_my_subreddits(limit=None)
	subreddits = [subreddit for subreddit in subreddits]

	r.login(config['to']['user'], config['to']['passwd'])
	
	print 'Unsubscribing from undesired defaults.'
	defaults = r.get_my_subreddits(limit=None)
	defaults = [default for default in defaults]
	for default in defaults:
		if default not in subreddits:
			print 'Unsubscribing from', default
			r.unsubscribe(default)
	
	print 'Subscribing to subreddits.'
	for subreddit in subreddits:
		if subreddit not in defaults:
			print 'Subscribing to', subreddit
			r.subscribe(subreddit)

if __name__ == '__main__':
	main()
