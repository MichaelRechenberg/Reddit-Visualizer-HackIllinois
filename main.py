# Reddit visualizer for HackIllinois 2016
#
# Author: Michael Rechenberg

import praw
import re

print "Starting\n"

user_agent = "HackIllinois 2016 Reddit Scraper u/MikeandOrIke"

#Make our Reddit object with the string as our user agent
r = praw.Reddit(user_agent)

#get a random subreddit
randomSub = r.get_random_subreddit(nsfw=False)
print randomSub

#Get the ID's of the subreddit's front page
url = "https://www.reddit.com/r/{0}/.json".format(str(randomSub))
derp = r.request(url)
#dictionary holding our json
data = derp.json()

#Add all the thread id's of the front page of the
# subreddit to idArr
idArr = []
for x in data['data']['children']:
    idArr.append(x['data']['id'])

# req = urllib2.Request(url, headers={'User-Agent': user_agent})
# html = urllib2.urlopen(req).read()
# print html

commentList = []

for subID in idArr:
    #access the submission with the given submission ID
    submission = r.get_submission(submission_id=subID)
    #expand MoreCommentObjects
    submission.replace_more_comments(limit=None, threshold=0)
    #make it an unordered list instead of a tree
    comments = praw.helpers.flatten_tree(submission.comments)

    for x in comments:
        commentList.append(x.body)


keyword = raw_input("Enter the word you want to search for (Case Insensitive)\n")

#count how many times the word was found in the comments
#only counts one word per comment to prevent spammers from
#   skewing results
#use re's findall if I want to count multiple words
wordCount = 0

for comment in commentList:
    comment = comment.lower()
    if re.search(r"\b{0}\b".format(keyword), comment) != None:
        print comment
        wordCount += 1

print wordCount



print "Finished!"