from mycroft import MycroftSkill, intent_file_handler


class Schoolmanager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('schoolmanager.intent')
    def handle_schoolmanager(self, message):
        self.speak_dialog('schoolmanager')


def create_skill():
    return Schoolmanager()

