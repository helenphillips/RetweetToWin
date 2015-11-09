import os, time, sys, random

sys.path.append("/Users/Helen/PythonLibraries/python-twitter")

import twitter

os.chdir('/Users/Helen/twitter/RetweetToWin')

from twitterlogon import *

search_terms = ('RTtowin', 'WinitWednesdays','freebiefriday','giveaway', 'RT+Follow', 'follow & RT', 'FLW & RT')
# perform the search

# grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
LATESTFILE = 'rt2win_latest.txt'

if os.path.exists(LATESTFILE):
    fp = open(LATESTFILE)
    lastid = fp.read().strip()
    fp.close()

    if lastid == '':
        lastid = 0
else:
    lastid = 0


for term in search_terms: 
    print 'Searching for %s' % term
    results = api.GetSearch(term, count=20, since_id=lastid)
    print 'Found %s results.' % (len(results))

    if len(results) > 0:
        fp = open(LATESTFILE, 'w')
        fp.write(str(max([x.id for x in results])))
        fp.close()

    for statusObj in results:
        print statusObj.retweet_count
        if statusObj.retweet_count > 4 and '@_philpots' not in statusObj.text.lower() and '@_philpots' not in statusObj.user.screen_name:
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


    