import pytest
from datetime import datetime, timedelta
import re
from utilities import Flight_utility, InsufficientPlace

@pytest.fixture
def flightutils():
    return Flight_utility()

@pytest.fixture
def ticket():
    return Flight_utility(20)

@pytest.fixture
def passwordCheck():
    return Flight_utility()

def test_flight_duration(flightutils):
    #flightutils.calculFlightDuration('')
    actualvalueflightduration=flightutils.calculFlightDuration(datetime.strptime('2025-06-09 13:22:34', '%Y-%m-%d %H:%M:%S'))
    expectedvalueflightduration=datetime.strptime('2025-06-09 13:22:34', '%Y-%m-%d %H:%M:%S')-datetime.now()
    assert abs(expectedvalueflightduration.total_seconds()-actualvalueflightduration.total_seconds()) < 3

def test_check_order_validity(ticket):
    ticket.check_order_validity(10)
    assert ticket.place > 0

def testcheck_password_validity(flightutils):
    ticket.check_order_validity('12345')
    assert ticket.place > 0



