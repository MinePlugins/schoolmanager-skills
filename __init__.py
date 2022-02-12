from mycroft import MycroftSkill, intent_file_handler

import requests
import datetime
from dateutil import parser
import pytz
import dateparser

utc=pytz.UTC






class Schoolmanager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('schoolmanager.intent')
    def handle_schoolmanager(self, message):
        date = self.get_response('Donne moi une date ?')
        date = dateparser.parse(date)
        self.log.info(f'Date parser :{date}')
        promo = self.get_response('quel.est.ta.promo ?')

        self.speak_dialog(self.get_cours(promo, date))

    def get_cours(self, promo, dateuser):
        r = requests.get(f'https://schoolmanager.cfa-insta.fr:3030/api/promotion/{promo}/planning', verify=False)
        data = r.json()
        now = datetime.datetime.now()
        cours = None
        for i in data['response']:
            
            date = parser.parse(i['module_date'])
            hourf = parser.parse(i['time_start'])
            houre = parser.parse(i['time_end'])
            hourf = hourf.replace(day=date.day,month=date.month,year=date.year)
            houre = houre.replace(day=date.day,month=date.month,year=date.year)
            if (date.month == dateuser.month and date.day == dateuser.day and date.year == dateuser.year):
                dateuser = dateuser.replace(hour=9, minute=5)
                self.log.info(f'Date == :{dateuser}')
                self.log.info(f'Date == :{hourf}')
                self.log.info(f'Date == :{houre}')

                if hourf <= dateuser <= houre:
                    cours = i['name']

        if cours is not None:
            return cours
        else: 
            return "Tu n'as aucun cours "

def create_skill():
    return Schoolmanager()

