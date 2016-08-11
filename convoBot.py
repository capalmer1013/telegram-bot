import nltk
import re
import objects
# from twitter import *
import twitter
from firebase import firebase
import random
from nltk.corpus import treebank
import json

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

firebase = firebase.FirebaseApplication('https://hackbotai.firebaseio.com/', None)

fetchTweets = False


def cleanTweets(inputTweet):
    inputTweet = re.sub(r'https?:\/\/.*[\r\n]*', '', inputTweet)

    inputTweet = inputTweet.replace('(', '')
    inputTweet = inputTweet.replace(')', '')
    inputTweet = inputTweet.replace('"', '')
    inputTweet = inputTweet.replace(' / ', '')

    if '@' in inputTweet:
        while '@' in inputTweet:
            index = inputTweet.index('@')
            i = index
            while i < len(inputTweet) and inputTweet[i] != ' ':
                i += 1

            inputTweet = inputTweet[:index] + inputTweet[i - 1:]

            if '@ ' in inputTweet:
                inputTweet = inputTweet[:index] + inputTweet[index+1:]
    return inputTweet


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]



print 'Generating tweet'
G = objects.weightedGraph()

nltk.data.path.append('/run/media/cpalmer/WD/nltk_data')
pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

listOfSentences = []

for status in statuses:
    a = cleanTweets(status)
    if len(a) > 0:
        listOfSentences.append(cleanTweets(status))


listOfWords = []
listOfTokens = []
listOfTaggedTokens = []
listOfSentenceTags = []
listOfTaggedWords = []

for sentence in listOfSentences:
    listOfTokens.append(nltk.word_tokenize(sentence))

for token in listOfTokens:
    listOfTaggedTokens.append(nltk.pos_tag(token))


for sentenceTag in listOfTaggedTokens:
    tempList = []
    for word in sentenceTag:
        if word not in listOfWords:
            listOfWords.append(word)

        tempList.append(word[1])
    if tempList not in listOfSentenceTags:
        listOfSentenceTags.append(tempList)

for sentence in listOfTokens:
    prevWord = ''
    for word in sentence:
        if 'http' not in word and '://' not in word:
            if word not in G.states:
                G.states.append(word)
            if prevWord == '':
                prevWord = word
                G.trainStart(word)
            else:
                G.train(prevWord, word)
                prevWord = word

for taggedTokens in listOfTaggedTokens:
    for token in taggedTokens:
        if token not in listOfTaggedWords:
            listOfTaggedWords.append(token)
print 'tweeting'
newlist = []

for word in listOfWords:
    newlist.append(word[0])

def generateResponse():
    tweet = G.generateSentence(listOfTaggedWords, listOfSentenceTags)
    while len(tweet) < 20:
        tweet = G.generateSentence(listOfTaggedWords, listOfSentenceTags)

    print '----------------------------------'
    print tweet
    listofAts = find(tweet, '@')
    for index in listofAts:
        tweet = tweet[:index]+tweet[index+1:]
    tweet = tweet.replace('# ', '#')
    tweet = tweet.replace(' .', '.')
    tweet = tweet.replace(' ,', ',')
    tweet = tweet.replace(' !', '!')
    tweet = tweet.replace(' :', ':')
    tweet = tweet.replace(' ?', '?')
    tweet = tweet.replace(" '", "'")
    tweet = tweet.replace("' ", "'")
    tweet = tweet.replace(' ;', '')
    tweet = tweet.replace('& amp', '&')
    tweet = tweet.replace('rt: ', '')
    tweet = tweet.replace('RT: ', '')
    oldTweet = ''
    while oldTweet != tweet:
        oldTweet = tweet
        tweet = re.sub(r'^[^iIaA\w] ', '', tweet)
        tweet = re.sub(r' [^iIaA\w] ', ' ', tweet)

    tweet = tweet.strip()
    if len(tweet) > 140:
        tweet = tweet[:140]

    tweet = tweet.strip()

    # tempstring = nltk.wordpunct_tokenize(tweet)
    tempstring = nltk.word_tokenize(tweet)
    # tempstring = tweet.split()

    if tempstring[-1] not in newlist:
        tweet = tweet[:-len(tempstring[-1])]

    if 140 - len(tweet) >= len(currentTrend):
        tweet += currentTrend
	return tweet

tweet = generateResponse()



