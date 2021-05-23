from datetime import datetime
from threading import Thread
import os
import pickle
import base64
from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from django.conf import settings

class MailSender:
    refMail = ""

    def start_new_thread(function):
        def decorator(*args, **kwargs):
            t = Thread(target = function, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()
        return decorator

    @start_new_thread
    def sendMail(message):
        now = datetime.now()
        receiver = "bicskow@gmail.com"
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(settings.BASE_DIR, 'token.pickle')):
            with open(os.path.join(settings.BASE_DIR, 'token.pickle'), 'rb') as token:
                creds = pickle.load(token)

            service = build('gmail', 'v1', credentials=creds)
            message = MailSender.create_message("me", receiver, "Gate triggered", f"{message}: {now}")
            MailSender.send_message(service, "me", message)

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
        message['threadId']='gateOpener'
        if MailSender.refMail:
            message['In-Reply-To']=f'<{MailSender.refMail}@mail.gmail.com>'
            message['References']=f'<{MailSender.refMail}@mail.gmail.com>'
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
            if not MailSender.refMail:
                MailSender.refMail= message['id']
            return message
        except errors.HttpError as error:
            print(f'An error occurred: {error}')