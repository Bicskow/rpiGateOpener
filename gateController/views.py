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
    if request.method =='POST':
        command = request.POST.get('command', '')
        if command == "pedestrian_access":
            led = LED(2, active_high=False)
            led.on()
            sleep(0.5)
            led.off()
            led.close()
            return HttpResponse(status=200)
        elif command == "vehicle_access":
            led = LED(3, active_high=False)
            led.on()
            sleep(0.5)
            led.off()
            led.close()
            return HttpResponse(status=200)
    return HttpResponseBadRequest(status=400)
    
