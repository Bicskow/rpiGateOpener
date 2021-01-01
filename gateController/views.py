from django.shortcuts import render
from django.http import HttpResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from gpiozero import LED
from time import sleep
import yagmail
from datetime import datetime
from threading import Thread
import os

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
                sleep(0.5)
                led.off()
                led.close()
                sendMail("Pesestrian access triggered")
                return HttpResponse(status=200)
            elif command == "vehicle_access":
                led = LED(3, active_high=False)
                led.on()
                sleep(0.5)
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
    receiver = ["bicskow@gmail.com", "csilla.pszabo@gmail.com"]
    yag = yagmail.SMTP(user="bicskowpi", oauth2_file=os.path.join(settings.BASE_DIR, 'client_secret.json'))
    yag.send(
        to=receiver,
        subject=f"Gate triggered",
        contents=f"{message}: {now}", 
    )
