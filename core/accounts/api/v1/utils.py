import threading


class EmailThread(threading.Thread):

    # this class use multi threading for sending email faster

    def __init__(self, email_obj):
        super().__init__()
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
