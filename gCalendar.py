from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import icalendar
import json

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentialsgameofficials.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '/tmp/key.json'
APPLICATION_NAME = 'gameofficials'

class gCalendar:

    def __init__(self):
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http, cache_discovery=False)


    def get_credentials(self):
 
        store = Storage(CLIENT_SECRET_FILE)
        credentials = store.get()
        return credentials


    def addEvent(self, icsData, checkForExisting=False):
        event = self.icsToEvent(icsData)
        if not self.eventExists(event['description']):
            event = self.service.events().insert(calendarId='primary', body=event).execute()


    def eventExists(self, game):
        # parse 'game' for the game number, then see if we can find that already in the calendar
        gStart = game.find("[Game: ")
        gStart += len("[Game: ")
        gEnd = game.find(']')
        gEnd = len(game) - gEnd
        gId = game[gStart:-gEnd]
        #searchString = '"[Game: {0}]"'.format(gId)
        searchString = game
        searchString = game.split("\n")[0]
        print("searchstring = {0}".format(searchString))
        # only start looking from the beginning of this month as game number from previous years recycle
        now = datetime.datetime.utcnow()
        now = now.replace(day=1)
        timemin = now.isoformat() + 'Z'
        print ("checking for game id: {0}".format(gId))
        events = self.service.events().list(calendarId='primary', timeMin=timemin, q=searchString).execute()
        #print ("game found? {0}".format(len(events['items']) > 0))
        if len(events['items']) > 0:
            for item in events['items']:
                #print ("*******************************************************")
                print ("Found existing game")
                #if 'description' in item:
                #    print (item['description'])
                #else:
                #    print ("No Description")
                #print ("*******************************************************")
        else:
            print("did not find existing game for game id: {0}".format(gId))
        return len(events['items']) > 0

    def icsToEvent(self, icsData):
        calendar = icalendar.Calendar.from_ical(icsData)
        for entry in calendar.walk('VEVENT'):
            return { 'summary': entry['SUMMARY'],
                     'location': entry['LOCATION'],
                     'description': entry['DESCRIPTION'],
                     'start': { 'dateTime': entry['DTSTART'].dt.strftime('%Y-%m-%dT%H:%M:%S-00:00'),
                                'timeZone': "UTC"
                     },
                     'end': { 'dateTime': entry['DTEND'].dt.strftime('%Y-%m-%dT%H:%M:%S-00:00'),
                              'timeZone': "UTC"
                     }
            }

