# Reddit visualizer for HackIllinois 2016
#
# Author: Michael Rechenberg

import praw
import re
from flask import Flask, jsonify, Response, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#http://stackoverflow.com/questions/23066488/json-passed-from-python-flask-into-javascript-is-displaying-on-screen
@app.route('/ajax')
def ajax():
    return Response(jsonify(redditCode()), mimetype='application/json')

def redditCode():
    print "Starting\n"

    user_agent = "HackIllinois 2016 Reddit Scraper u/MikeandOrIke"

    #Make our Reddit object with the string as our user agent
    r = praw.Reddit(user_agent)


    #Get the ID's of the subreddit's front page
    #Variable to hold the HTTP response
    response = None
    url = ""
    while True:
        subreddit = raw_input("What subreddit would you like to search?\n")
        url = "https://www.reddit.com/r/{0}/.json".format(str(subreddit))
        try:
            response = r.request(url, retry_on_error=False)
            print "Good choice!"
            break
        except (praw.errors.InvalidSubreddit):
            print "Invalid subreddit, try again"

    #dictionary holding our json
    data = response.json()

    #Add all the thread id's of the front page of the
    # subreddit to idArr
    idArr = []
    for x in data['data']['children']:
        idArr.append(x['data']['id'])

    # req = urllib2.Request(url, headers={'User-Agent': user_agent})
    # html = urllib2.urlopen(req).read()
    # print html

    print "Gathering Comments"
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

    #count how many a word was found in the comments
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

    result = {}
    result[keyword] = wordCount
    print result
    return result


if(__name__ == "__main__"):
    app.run(debug=True)