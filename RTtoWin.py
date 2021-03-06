import os, time, sys, random

if os.uname()[1] == "Helen-Phillipss-MacBook-Pro.local":
    sys.path.append("/Users/Helen/PythonLibraries/python-twitter")
    import twitter
    os.chdir('/Users/Helen/twitter/RetweetToWin')

if os.uname()[1] == "raspberrypi":
    sys.path.append("/home/pi/PythonLibraries/python-twitter")
    import twitter
    os.chdir('/home/pi//RetweetToWin')
    import requests
    requests.packages.urllib3.disable_warnings()

from twitterlogon import *

search_terms = ('RTtowin', 'WinitWednesdays','freebiefriday','giveaway', 'RT+Follow', 'follow & RT')
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


for term in search_terms: 
    print bcolors.OKBLUE + 'Searching for %s' % term + bcolors.ENDC
    results = api.GetSearch(term, count=20, since_id=lastid)
    print 'Found %s results.' % (len(results))

    if len(results) > 0:
        fp = open(LATESTFILE, 'w')
        fp.write(str(max([x.id for x in results])))
        fp.close()

    for statusObj in results:
        # print statusObj.retweet_count
        if statusObj.retweet_count > 10 and '@_philpots' not in statusObj.text.lower() and '@_philpots' not in statusObj.user.screen_name and 'followback' not in statusObj.text.lower():
            try:
                print bcolors.OKGREEN + 'Retweeting @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace')) + bcolors.ENDC
                rt_id = statusObj.id
                api.PostRetweet(original_id = rt_id) 

                print bcolors.OKGREEN + 'Following @%s' % (statusObj.user.screen_name.encode('ascii', 'replace'))  + bcolors.ENDC
                user = statusObj.user.screen_name.encode('ascii', 'replace')
                api.CreateFriendship(statusObj.user.id)

                if len(statusObj.user_mentions) > 0:
                    for mentions in statusObj.user_mentions:
                        print bcolors.OKGREEN + 'Also following @%s'  % (mentions.name) + bcolors.ENDC
                        api.CreateFriendship(mentions.id)

                time.sleep(1)
            except Exception:
                print "Unexpected error:", sys.exc_info()[0:2]


    