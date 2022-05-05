__author__ = 'fatihsamet'

import sys
import tweepy
import xml.etree.ElementTree as ET
dictTweets = {}
def get_content(argv,ids):
    auth = tweepy.OAuthHandler(argv[3], argv[4])
    auth.set_access_token(argv[1], argv[2])
    api = tweepy.API(auth)
    i = 0
    lst = []
    for id in ids:
        lst.append(id)
        i = i+1
        if i >= 99:
            try:
                tweets = api.statuses_lookup(lst);
                for tweet in tweets:
                    dictTweets[str(tweet.id)] = tweet.text
            except tweepy.error.TweepError as e:
                code = e.message[0][u'code']
                print e.message[0]
                raise
            lst = []
            i = 0


def main(argv):
    tree = ET.parse('telecom_train_turkish_final.xml')
    root = tree.getroot()
    fullIds = []
    for child in root:
        tweetid = child.attrib["tid"]
        fullIds.append(tweetid)
    get_content(argv,ids=fullIds)
    for child in root:
        tweetid = child.attrib["tid"]
        text = '**DELETED**'
        if tweetid in dictTweets:
           text = dictTweets[tweetid]
        child[0].text = text
        for ichild in child[1]:
            target = "**DELETED**"
            if tweetid in dictTweets:
                frm = int(ichild.attrib["from"])
                to = int(ichild.attrib["to"])
                target = text[frm:to]
            ichild.set("atarget", target)
            ichild.set("bcategory", ichild.attrib["category"])
            ichild.set("cpolarity", ichild.attrib["polarity"])
            ichild.set("dfrom", ichild.attrib["from"])
            ichild.set("eto", ichild.attrib["to"])
            del ichild.attrib["target"]
            del ichild.attrib["category"]
            del ichild.attrib["polarity"]
            del ichild.attrib["from"]
            del ichild.attrib["to"]


    tree.write("telecom_train_turkish_final_unmasked.xml",encoding="UTF-8")
    content = ''
    with open("telecom_train_turkish_final_unmasked.xml",'r') as f:
        content = f.read()
        content = content.replace("atarget","target").replace("bcategory","category").replace("cpolarity","polarity").replace("dfrom","from").replace("eto","to")
    with open("telecom_train_turkish_final_unmasked.xml",'w') as f:
        f.write(content)
    print 'Tweets are collected successfully'

if __name__ == "__main__":
    main(sys.argv)