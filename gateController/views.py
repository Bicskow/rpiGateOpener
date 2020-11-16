from django.shortcuts import render
from django.http import HttpResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from gpiozero import LED
from time import sleep

@ensure_csrf_cookie
def index(request):
    return render(request, 'gateController/gateController.html')

def triggerGate(request):
    led = LED(5)
    led2 = LED(27)
    led.off()
    led2.off()

    if request.method =='POST':
        command = request.POST.get('command', '')
        if command == "pedestrian_access":
            led.on()
            sleep(0.5)
            led.off()
            le2.off()
            return HttpResponse(status=200)
        elif command == "vehicle_access":
            led2.on()
            sleep(0.5)
            led.off()
            le2.off()
            return HttpResponse(status=200)

    led.off()
    led2.off()
    return HttpResponseBadRequest(status=400)
    
