from twilio.rest import Client
from decouple import config
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def send_message(code_user, phone_number):
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"Hi! Your user and verification code is:\n {code_user}",
                        from_='+18507417434',
                        to=f'{phone_number}'
                    )

    return message.sid

def send_email(username, code, user_email):
    subject = 'OTP Verification'
    message = f"\n\nYour verification code for {username} at A-M-A Blog is {code}.\nIt is only valid for one login.\n"
    try:
        send_mail(subject, message, 'amablogteam@gmail.com', [user_email,])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')