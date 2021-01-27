from django.shortcuts import render
from django.http import HttpResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from gpiozero import LED
from time import sleep
from datetime import datetime
from threading import Thread
import os
import pickle
import base64
from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build

@ensure_csrf_cookie
def index(request):
    return render(request, 'gateController/gateController.html')

def triggerGate(request):
    try:
        if request.method =='POST':
            command = request.POST.get('command', '')
            if command == "pedestrian_access":
                led = LED(2, active_high=False)
                led.on()
                sleep(0.2)
                led.off()
                led.close()
                sendMail("Pedestrian access triggered")
                return HttpResponse(status=200)
            elif command == "vehicle_access":
                led = LED(3, active_high=False)
                led.on()
                sleep(0.2)
                led.off()
                led.close()
                sendMail("Vehicle access triggered")
                return HttpResponse(status=200)
        sendMail("Gate trigger failed with bad request")
        return HttpResponseBadRequest(status=400)
    except Exception as e:
        sendMail(f"Gate trigger failed with exception: {e}")
        return HttpResponseServerError(status=500)

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@start_new_thread
def sendMail(message):
    now = datetime.now()
    receiver = "bicskow@gmail.com, csilla.pszabo@gmail.com"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(settings.BASE_DIR, 'token.pickle')):
        with open(os.path.join(settings.BASE_DIR, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)

        service = build('gmail', 'v1', credentials=creds)
        message = create_message("me", receiver, "Gate triggered", f"{message}: {now}")
        send_message(service, "me", message)

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f"Message Id: {message['id']}")
        return message
    except errors.HttpError as error:
        print(f'An error occurred: {error}')
