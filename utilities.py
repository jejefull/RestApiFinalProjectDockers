from datetime import datetime, timedelta
import re

d1=datetime.now()
d2=datetime.now()+timedelta(days=1)
print(d2-d1)


class InsufficientPlace(Exception):
    pass

'''
class Ticket(object):
    def __init__(self, initial_amount=0):
        self.balance = initial_amount


    def add_ticket(self, amount):
        self.balance += amount

    def spend_ticket(self, amount):
        if self.balance < amount:
            raise InsufficientAmount('Not enough available to spend {}'.format(amount))
        self.balance -= amount


    def check_password_validity(self, chekPassword):
        pattern = "^.*(?=.{7,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        if re.findall(pattern, chekPassword):
            True
        else:
            False
'''


class Flight_utility(object):

    def calculFlightDuration(self, landing_date):
        ini_time_for_now = datetime.now()
        return (landing_date - ini_time_for_now)

    def check_password_validity(self, password_check):
        return (password_check)
        pattern = "^.*(?=.{7,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        if re.findall(pattern, chekPassword):
            True
        else:
            False

    def __init__(self, initial_place=0):
        self.place = initial_place

    def add_ticket(self, initial_place):
        self.place += place

    def check_order_validity(self, initial_place):
        if self.place < initial_place:
            raise InsufficientPlace('Not enough available to spend {}'.format(initial_place))
        self.place -= initial_place




