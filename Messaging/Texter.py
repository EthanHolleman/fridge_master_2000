from twilio.rest import Client
import os

# TWILIO information, from env variables assigned below
NUMBER = os.environ.get('NUMBER')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
ACCOUNT_SID = os.environ.get('FRIDGE_SID')
AUTH_TOKEN = os.environ.get('FRIDGE_AUTH')


def get_client():
    return Client(ACCOUNT_SID, AUTH_TOKEN)


def compose_warnings(emergency_temp=False,
                     emergency_fridge=False,
                     emergency_freezer=False,
                     temp=None,
                     open_time=None):

    message_base = 'BEEP BEEP\nFridge Master 2000 Warning\n'
    warning = ''
    if emergency_temp is True:
        warning = '{}Temp is above 60, currently @ {}'.format(message_base, temp)
    elif emergency_fridge is True:
        warning = '{}Fridge open for > 15 mins, currently open for {}'.format(
            message_base, open_time)
    elif emergency_freezer is True:
        warning = '{}Freezer open for > 15 mins, currently open for {}'.format(
            message_base, open_time)
    return warning


def send_warnings(message, client):
    print(message)
    client.messages.create(body=message, from_=TWILIO_NUMBER, to=NUMBER)
