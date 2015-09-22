import os, time, sys, random

sys.path.append("/Users/Helen/PythonLibraries/python-twitter")

import twitter

os.chdir('/Users/Helen/twitter/RetweetToWin')

from twitterlogon import *

LATESTFILE = 'rt2win_latest.txt'
# LOGFILE = 'rt2win_log.txt'




# grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
if os.path.exists(LATESTFILE):
    fp = open(LATESTFILE)
    lastid = fp.read().strip()
    fp.close()

if lastid == '':
    lastid = 0
else:
    lastid = 0

# perform the search
results = api.GetSearch('RT to win', since_id=lastid)
print 'Found %s results.' % (len(results))
if len(results) == 0:
    print 'Nothing to reply to. Quitting.'
    sys.exit()
repliedTo = []
if len(results) > (len(statuses) * 2):
    results = random.sample(results, (len(statuses) * 2))



for statusObj in results:
    statusObj.created_at = statusObj.created_at[:-11] + statusObj.created_at[25:]
    postTime = time.mktime(time.strptime(statusObj.created_at, '%a %b %d %H:%M:%S %Y'))

    if time.time() - (24*60*60) < postTime and statusObj.retweeted == False and '@_philpots' not in statusObj.text.lower():
       # if [True for x in alreadyMessaged if ('@' + x).lower() in statusObj.text.lower()]:
       #     print 'Skipping because it\'s a mention: @%s - %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
       #     continue

        try:
            print 'Posting in reply to @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            api.PostUpdate('@%s' % (statusObj.user.screen_name) + statuses[randint(1, len(statuses))] , in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('ascii', 'replace').replace('\n','').replace('\r','') ))
            time.sleep(1)
        except Exception:
            print "Unexpected error:", sys.exc_info()[0:2]


fp = open(LATESTFILE, 'w')
fp.write(str(max([x.id for x in results])))
fp.close()