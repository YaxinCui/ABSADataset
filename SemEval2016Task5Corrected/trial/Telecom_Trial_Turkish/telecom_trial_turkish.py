__author__ = 'fatihsamet'

import sys
import tweepy
import xml.etree.ElementTree as ET

def get_content(argv,tid):
    auth = tweepy.OAuthHandler(argv[3], argv[4])
    auth.set_access_token(argv[1], argv[2])
    api = tweepy.API(auth)
    try:
        tweet = api.get_status(id =tid)
        return tweet.text
    except tweepy.error.TweepError as e:
        if(e.message[0][u'code'] == 144):
            return None
        else:
            raise

def main(argv):
    tree = ET.parse('telecom_trial_turkish_final.xml')
    root = tree.getroot()
    for child in root:
        tweetid = child.attrib["tid"]
        tweet = get_content(argv,tid=tweetid)
        if(tweet is None):
            child[0].text = "**DELETED**"
        else:
            child[0].text = tweet
        for ichild in child[1]:
            if tweet is None:
                target = "**DELETED**"
            else:
                frm = int(ichild.attrib["from"])
                to = int(ichild.attrib["to"])
                target = tweet[frm:to]
            ichild.attrib["target"] = target
    tree.write("telecom_trial_turkish_final_unmasked.xml",encoding="UTF-8")
    print 'Tweets are collected successfully'

if __name__ == "__main__":
    main(sys.argv)