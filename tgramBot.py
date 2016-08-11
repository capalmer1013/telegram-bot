#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys
import random
import re
import convoBot

sys.path.insert(0, "../poetry")
sys.path.insert(0, "../natural-language")

import tweeter
import writePoem
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

punctuation = ['.', '.', '', '!', '?', '', '', '.', '.', '.'] 
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="you're a cunt")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def kill(bot, update):
    bot.sendMessage(update.message.chat_id, text="Too Many Humans")
    
def fuck(bot, update):
    botResponse = "fuck you mate"
    print "fuck"
    bot.sendMessage(update.message.chat_id, text=botResponse)

def shit(bot, update):
    bot.sendMessage(update.message.chat_id, text=botResponse)

def poem(bot, update):
    print "writing poem"
    listOfSpeakingLines = []
    botResponse = ''
    bot.sendMessage(update.message.chat_id, text="alright give me a fuckin second...")
    
    listOfLines = writePoem.writePoem()
    while len(listOfLines) > 20:
        listOfLines = writePoem.writePoem()
        
    for line in listOfLines:
        listOfSpeakingLines.append(re.findall('[A-Z][^A-Z]*', line))
    for lineList in listOfSpeakingLines:
        for line in lineList:
            line = line.rstrip()
            line += punctuation[random.randint(0, len(punctuation)-1)]
            botResponse += (line + '\n')

    bot.sendMessage(update.message.chat_id, text=botResponse)

def drink(bot, update):
    listOfLines = writePoem.writePoem()
    listOfSpeakingLines = []
    possibleLines = []
    
    while len(listOfLines) > 20:
        listOfLines = writePoem.writePoem()
        
    for line in listOfLines:
        listOfSpeakingLines.append(re.findall('[A-Z][^A-Z]*', line))
        
    for lineList in listOfSpeakingLines:
        for line in lineList:
            line = line.rstrip()
            line += punctuation[random.randint(0, len(punctuation)-1)]
            possibleLines.append(line)
            
    botResponse = possibleLines[random.randint(0, len(possibleLines)-1)]
    bot.sendMessage(update.message.chat_id, text=botResponse)
    
def yiff(bot, update):
    botResponse = "furry trash"
    bot.sendMessage(update.message.chat_id, text=botResponse)
    
def tweet(bot, update):
    botResponse = tweeter.generateTweet()
    bot.sendMessage(update.message.chat_id, text=botResponse)
    
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("266646927:AAFJD84hNXfo3dLtiJbaOkixEeh-BZZYvmE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("kill", kill))
    dp.add_handler(CommandHandler("fuck", fuck))
    dp.add_handler(CommandHandler("poem", poem))
    dp.add_handler(CommandHandler("drink", drink))
    dp.add_handler(CommandHandler("yiff", yiff))
    dp.add_handler(CommandHandler("tweet", tweet))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
