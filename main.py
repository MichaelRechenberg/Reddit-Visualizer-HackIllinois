import praw

print "Starting\n"

user_agent = "HackIllinois 2016 Reddit Scraper u/MikeandOrIke"

#Make our Reddit object with the string as our user agent
r = praw.Reddit(user_agent)

#Get the ID's of the page's threads
url = "https://www.reddit.com/r/uiuc/.json"
derp = r.request(url)
#dictionary holding our json
data = derp.json()

idArr = []

for x in data['data']['children']:
    idArr.append(x['data']['id'])


#Access html

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

    #write the comment to a text file
    for x in comments:
        commentList.append(x.body)

for com in commentList:
    print com
randomSub = r.get_random_subreddit(nsfw=False)
print randomSub


subreddit = r.get_subreddit(str(randomSub))

# all_comments = r.get_comments("funny", limit=0)
# for x in all_comments:
#     print x.body



print "done"