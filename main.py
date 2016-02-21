# Reddit comment for HackIllinois 2016
#
# Searches through a subreddit's front-page threads and
#   prints out how many times the keyword was found a comment
# The searches are case insensitive
#
# Author: Michael Rechenberg

import praw
import re
from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup
import urllib2


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

#http://stackoverflow.com/questions/23066488/json-passed-from-python-flask-into-javascript-is-displaying-on-screen
@app.route('/ajax')
def ajax():

    #array to hold all of the keywords we want to use
    keywords = []
    #extract arguments from query string
    keywordCount = int(request.args.get('keywordCount'))
    for x in xrange(keywordCount):
        str = "keyword{0}".format(x)
        keyword = request.args.get(str)
        keywords.append(keyword)

    subreddits = []
    subredditCount = int(request.args.get('subredditCount'))
    for x in xrange(subredditCount):
        str = "subreddit{0}".format(x)
        subreddit = request.args.get(str)
        subreddits.append(subreddit)

    #send the work to the scraper
    result = redditCode(keywords, subreddits)
    #the user entered an invalid subreddit
    if result==None:
        return "InvalidSubreddit"
    return jsonify(result)


#inputKeywords: array of keywords we want to search
#inputSubreddit: subreddit we want to search
def redditCode(inputKeywords, inputSubreddits):
    print "Starting\n"

    user_agent = "HackIllinois 2016 Reddit Scraper u/MikeandOrIke"

    #Make our Reddit object with the string as our user agent
    r = praw.Reddit(user_agent)


    #Get the ID's of the subreddit's front page

    #Variable to hold the HTTP response
    response = None
    url = ""




    #Dictionary to contain how many times the word was found
    result = {}
    for keyword in inputKeywords:
        result[keyword] = 0

    #For every subreddit we want to search
    for subreddit in inputSubreddits:

        url = "https://www.reddit.com/r/{0}/.json".format(str(subreddit))
        try:
            response = r.request(url, retry_on_error=False)
            print "Searching the subreddit {0}.".format(subreddit)
        #Handle incorrect subreddits
        except (praw.errors.InvalidSubreddit):
            print "Invalid subreddit, try again"
            return None

        #dictionary holding our json
        data = response.json()

        #Add all the thread id's of the front page of the
        # subreddit to idArr
        idArr = []
        for x in data['data']['children']:
            idArr.append(x['data']['id'])

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

        print "Done Gathering Comments"
         #for every keyword
        for keyword in inputKeywords:
            print "Searching for {0}.".format(keyword)
            wordCount = 0
            #count how many a word was found in the comments
            #only counts one word per comment to prevent spammers from
            #   skewing results
            #use re's findall if I want to count multiple words

            for comment in commentList:
                comment = comment.lower()
                if re.search(r"\b{0}\b".format(keyword), comment) != None:
                    wordCount += 1
            result[keyword] += wordCount

    print "Finished!"


    print result
    return result


if(__name__ == "__main__"):
    app.run(debug=True)