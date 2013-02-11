# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()

    def is_word_in(self,text):
        text = text.lower()
        for i in string.punctuation:
            text = text.replace(i," ")
        text = text.split()
        if self.word in text:
            return True
        else:
            return False

        
        
        

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self,word)
        
    def is_word_in_title(self, title):
        return self.is_word_in(title)

    def evaluate(self, story):
        title = story.get_title()
        return self.is_word_in_title(title)


        
    
class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self,word)
        
    def is_word_in_subject(self, subject):
        return self.is_word_in(subject)

    def evaluate(self, story):
        subject = story.get_subject()
        return self.is_word_in_subject(subject)
    

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self,word)
        
    def is_word_in_summary(self, summary):
        return self.is_word_in(summary)

    def evaluate(self, story):
        summary = story.get_summary()
        return self.is_word_in_summary(summary)


# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, otherTrigger):
        self.otherTrigger = otherTrigger

    def evaluate(self, story):
        return not self.otherTrigger.evaluate(story)
        
    

class AndTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        return self.Trigger1.evaluate(story) and self.Trigger2.evaluate(story)


class OrTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        return self.Trigger1.evaluate(story) or self.Trigger2.evaluate(story)

# Phrase Trigger


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        subject = story.get_subject()
        title = story.get_title()
        summary = story.get_summary()
        return (self.phrase in subject) or (self.phrase in title) or (self.phrase in summary)


#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    triggered_stories = []
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story) == True:
                triggered_stories.append(story)
            
        
    return triggered_stories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
        
    triggerList = []
    trigger_dict = {}
    for item in lines:
        l = item.split()
        if l[1] == "TITLE":
            trigger = TitleTrigger(l[2])
            trigger_dict[l[0]] = trigger
            
        elif l[1] == "SUBJECT":
            trigger = SubjectTrigger(l[2])
            trigger_dict[l[0]] = trigger
            
        elif l[1] == "PHRASE":
            trigger = PhraseTrigger(l[2])
            trigger_dict[l[0]] = trigger
            
        elif l[1] == "AND":
            trigger = AndTrigger(trigger_dict[l[2]],trigger_dict[l[3]])
            trigger_dict[l[0]] = trigger

        if l[0] == "ADD":
            for i in l[1:]:
                triggerList.append(trigger_dict[i])


    return triggerList

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    
import thread

def main_thread(p):
    
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
##    t1 = SubjectTrigger("Obama")
##    t2 = SummaryTrigger("MIT")
##    t3 = PhraseTrigger("Supreme Court")
##    t4 = OrTrigger(t2, t3)
##    triggerlist = [t1, t4]
##    
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)
        SLEEPTIME = 60 #seconds -- how often we poll
        print "Sleeping..."
        time.sleep(SLEEPTIME)

        
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

