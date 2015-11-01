import os, time, sys, random

sys.path.append("/Users/Helen/PythonLibraries/python-twitter")

import twitter

os.chdir('/Users/Helen/twitter/RetweetToWin')

from twitterlogon import *

search_terms = ('RTtowin', 'WinitWednesdays','competition','giveaway')
# perform the search
for term in search_terms: 
    print 'Searching for %s' % term
    results = api.GetSearch(term, count=20)
    print 'Found %s results.' % (len(results))

    for statusObj in results:
        if statusObj.text[0:2] != "RT" and statusObj.retweeted == False and '@_philpots' not in statusObj.text.lower() and '@_philpots' not in statusObj.user.screen_name:
            try:
                print 'Retweeting @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
                rt_id = statusObj.id
                api.PostRetweet(original_id = rt_id) 

                print 'Following @%s' % (statusObj.user.screen_name.encode('ascii', 'replace'))
                user = statusObj.user.screen_name.encode('ascii', 'replace')
                api.CreateFriendship(statusObj.user.id)

                if len(statusObj.user_mentions) > 0:
                    for mentions in statusObj.user_mentions:
                        print 'Also following @%s' % (mentions.name)
                        api.CreateFriendship(mentions.id)

                time.sleep(1)
            except Exception:
                print "Unexpected error:", sys.exc_info()[0:2]