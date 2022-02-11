from mycroft import MycroftSkill, intent_file_handler

import requests
import datetime
from dateutil import parser
import pytz
import dateparser

utc=pytz.UTC





def get_cours(promo, date):
    r = requests.get(f'https://schoolmanager.cfa-insta.fr:3030/api/promotion/{promo}/planning', verify=False)
    data = r.json()
    now = datetime.datetime.now()
    cours = None
    for i in data['response']:
        
        date = parser.parse(i['module_date'])
        hourf = parser.parse(i['time_start'])
        houre = parser.parse(i['time_end'])
        if (date.month == now.month and date.day == now.day and date.year == now.year):
            if hourf <= date <= houre:
                cours = i['name']

    if cours is not None:
        return cours
    else: 
        return "Tu nas aucun cours "
class Schoolmanager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('schoolmanager.intent')
    def handle_schoolmanager(self, message):
        date = self.get_response('Donne moi un date ?')
        date = dateparser.parse(date)
        promo = self.get_response('quel.est.ta.promo ?')

        self.speak_dialog(get_cours(promo, date))


def create_skill():
    return Schoolmanager()

