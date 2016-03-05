# -*- coding: utf8 -*-
import json
import os
import urllib2

class TedSubtitle(object):
  """docstring for TedSubtitle"""
  def __init__(self, startOfParagraph, startTime, duration, content):
    super(TedSubtitle, self).__init__()
    self.startOfParagraph = startOfParagraph
    self.startTime = startTime
    self.duration = duration
    self.content = content
    self.endTime = startTime + duration




class TedParagraph(object):
  """docstring for ClassName"""
  def __init__(self, arg):
    super(TedParagraph, self).__init__()
    self.arg = arg




def GetSubtitles(talkID, languageCode):
  subtitleUrl = "http://www.ted.com/talks/subtitles/id/%s/lang/%s" % (talkID, languageCode)
  response = urllib2.urlopen(subtitleUrl)
  html = response.read() 
  subtitles = json.loads(html)["captions"]
  tedSubtitles = []
  for subtitle in subtitles:
    tedSubtitle = TedSubtitle(subtitle["startOfParagraph"], subtitle["startTime"], subtitle["duration"], subtitle["content"])
    tedSubtitles.append(tedSubtitle)

  return tedSubtitles




def json2srt(subtitles):

  def conv(t):
    return '%02d:%02d:%02d,%03d' % (
        t / 1000 / 60 / 60,
        t / 1000 / 60 % 60,
        t / 1000 % 60,
        t % 1000)


  for i, item in enumerate(subtitles):
    print (i,
           conv(item.startTime),
           conv(item.startTime + item.duration - 1),
           item.content)

def difference( num1, num2 ):
  return abs( num1 - num2 )

def hasContainsEndMark(content):
  if len( content) < 2:
    return False

  endMarks = [ '.', '?', '!', '。', '？', '！' ]
  for i in endMarks:
    if content[-1].encode('utf8') == i:
      return True

  return False


def printSubtitles(subtitles):
 for i in range(len(subtitles)):
    print subtitles[i].startTime
    print subtitles[i].duration
    print subtitles[i].content.encode('utf8')
    print
    print

def ResetStartTime(arr):
  for i in range(len(arr)):
    arr[i].startTime -= arr[0].startTime
    arr[i].startTime /= 1000
    arr[i].duration /= 1000

  return arr

def hasEvenQuotes( content ):
  return content.count('"') % 2 == 0 

def hasPairChar( content ):
  leftChars =  [ u'「', u'(', u'（', u'{', u'【', u'｛', u'[']
  rightChars = [ u'」', u')', u'）', u'}', u'】', u'｝', u']']
  
  for i in range(len(leftChars)):
    if ( content.count(leftChars[i].encode('utf8')) == content.count(rightChars[i].encode('utf8')) ):
      return True

  return False

def isNewParagraph(isStartOfParagraph, sentence):
  maxCharInSentence = 50
  
  newParagraph = isStartOfParagraph
  newParagraph = newParagraph or len(sentence) > maxCharInSentence
  newParagraph = newParagraph and hasEvenQuotes(sentence)
  newParagraph = newParagraph and hasContainsEndMark(sentence)
  newParagraph = newParagraph and hasPairChar(sentence.encode('utf8'))
  newParagraph = newParagraph and len(sentence) != 0
  return newParagraph
  


talkURL = "http://www.ted.com/talks/richard_st_john_s_8_secrets_of_success"
##talkURL = "http://www.ted.com/talks/kenneth_cukier_big_data_is_better_data"
talkTitle = talkURL.split('/')[-1].replace('_',' ')

#print talkTitle
#print '\n\n'
command = "curl -s %s | grep source=facebook | awk -F '=' '{print $3}' | awk -F '&' '{print $1}'" % ( talkURL )
talkID = '49'#os.popen(command).readlines()[0].strip()
print "talkID :", talkID


chineselanguageCode = 'zh-tw'
englishlanguageCode = 'en'



engSubtitles = ResetStartTime(GetSubtitles( talkID, englishlanguageCode ))
chineseSubtitles = ResetStartTime(GetSubtitles( talkID, chineselanguageCode ))
charCount = 0

filteredEnglishSubtitles = []
filteredChineseSubtitles = []
englishSentence = ''
chineseSentence = ''

lastAddedChar = ' '


matchedIndexsAtEnglishSubtitles = []

idxForChineseSubtitles = 0
idxForEnglishSubtitles = 0
lengthForChineseSubtitles = len(chineseSubtitles)
lengthForEnglishSubtitles = len(engSubtitles)
durationTolerance = 1500

durationInParagraph = 0
firstSentenceInParagraph = True
if False:
  for i in engSubtitles:
    print i.startTime
    print i.duration
    print i.content.encode('utf8')
    print 
  exit(0)

print "-"*20






def Merge(subtitles):

  lastAddedIndex = 0
  durationInParagraph = 0
  startTimeInParagraph = 0


  sentence = ''

  lastAddedChar = ' '

  durationInParagraph = 0
  firstSentenceInParagraph = True
  filteredSubtitles = []
  for i in xrange(len(subtitles)):

    subtitle = subtitles[i]
    
    if firstSentenceInParagraph:
      if i == 0 or True:
        startTimeInParagraph = subtitle.startTime
      else:
        startTimeInParagraph = subtitles[i-1].startTime
      firstSentenceInParagraph = False

    if isNewParagraph(subtitle.startOfParagraph,sentence):
      sentence = sentence.replace('\n', '')
      filteredSubtitle = TedSubtitle( True, startTimeInParagraph, durationInParagraph, sentence )
      filteredSubtitles.append(filteredSubtitle)
      sentence = subtitle.content 

      startTimeInParagraph = 0
      durationInParagraph = 0
      firstSentenceInParagraph = True

      lastAddedIndex = i
    else:
      sentence += subtitle.content
      durationInParagraph = subtitle.endTime



  if lastAddedIndex < len(subtitles):
    subtitle = TedSubtitle( True, startTimeInParagraph, durationInParagraph, sentence )
    filteredSubtitles.append(subtitle)

  return filteredSubtitles



filteredChineseSubtitles = Merge(chineseSubtitles)
if False:
  printSubtitles(filteredChineseSubtitles)


idxForChineseSubtitles = 0
idxForEnglishSubtitles = 0
durationInParagraph = 0
startTimeInParagraph = 0
lengthForChineseSubtitles = len(filteredChineseSubtitles)
englishSentence = ''

while idxForChineseSubtitles < lengthForChineseSubtitles:
  chineseDuration = filteredChineseSubtitles[idxForChineseSubtitles].duration
  minDurationDifference = 10000
  currentDurationDifference = 0
 
  idxForLastEnglishSubtitles = idxForEnglishSubtitles

  while idxForLastEnglishSubtitles < lengthForEnglishSubtitles:
    durationInParagraph = engSubtitles[idxForLastEnglishSubtitles].endTime
    preDurationDifference = currentDurationDifference
    currentDurationDifference = chineseDuration - durationInParagraph

    if currentDurationDifference <= 0:
      if abs(preDurationDifference) < abs(currentDurationDifference):
        break
      else:
        idxForLastEnglishSubtitles += 1
        break

    idxForLastEnglishSubtitles += 1


  while idxForEnglishSubtitles < idxForLastEnglishSubtitles:
    englishSentence += engSubtitles[idxForEnglishSubtitles].content.replace('\n',' ') + ' '
    idxForEnglishSubtitles += 1


  print englishSentence
  print filteredChineseSubtitles[idxForChineseSubtitles].content.encode("utf8")
  print "\n\n"  

  englishSentence = ''
  idxForChineseSubtitles += 1

