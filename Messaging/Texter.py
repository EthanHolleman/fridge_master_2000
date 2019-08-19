from twilio.rest import Client
import os

# TWILIO information, from env variables assigned below
NUMBER = os.environ.get('NUMBER')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
ACCOUNT_SID = os.environ.get('FRIDGE_SID')
AUTH_TOKEN = os.environ.get('FRIDGE_AUTH')


def get_client():
    '''
    Uses the declared enviromental variables to return a Twilio Client object
    '''
    return Client(ACCOUNT_SID, AUTH_TOKEN)


def compose_warnings(emergency_temp=False,
                     emergency_fridge=False,
                     emergency_freezer=False,
                     temp=None,
                     open_time=None):
    '''
    Returns string with warning based on booleans given
    '''

    message_base = 'BEEP BOOP\nFridge Master 2000 Warning!\n'
    warning = ''
    if emergency_temp is True:
        warning = '{}Temp is currently @ {}'.format(message_base, temp)
    elif emergency_fridge is True:
        warning = '{}Fridge has been open for {} minutes'.format(
            message_base, float(open_time)/60)
    elif emergency_freezer is True:
        warning = '{}Freezer open for {} minutes'.format(
            message_base, float(open_time)/60)
    return warning


def send_warnings(message, client):
    '''
    Uses Twilio client to send SMS message
    '''
    print(message)
    client.messages.create(body=message, from_=TWILIO_NUMBER, to=NUMBER)
