import os
import mechanicalsoup
from shutil import copyfile
from gCalendar import gCalendar
from refWebSites import GameOfficials, MySoccerLeague


def checkWebsites():
    # Browser
    br = mechanicalsoup.StatefulBrowser(soup_config={ 'features': 'html.parser'})
    br.addheaders = [('User-agent', 'Chrome')]

    websites = []
    websites.append(GameOfficials(br))
    websites.append(MySoccerLeague(br))

    for website in websites:
        assignments = website.getAssignments()

        gc = gCalendar()
        for assignment in assignments:
            gc.addEvent(assignment)

def main(json_data, context):
    copyfile('./key.json', '/tmp/key.json')
    checkWebsites()
    return {
        'statusCode': 200,
        'message': "all is well",
        'body': 'None'
    }

# uncomment for local debugging
#main(0, 0)