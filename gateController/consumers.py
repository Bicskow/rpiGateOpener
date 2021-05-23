import json
from gpiozero import LED
from time import sleep
from channels.generic.websocket import WebsocketConsumer
from .mailSender import MailSender

class GateTriggerConsumer(WebsocketConsumer):
    def connect(self):
        sleep(0.5)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']

        self.triggerGate(command)
    
    def triggerGate(self, command):
        try:
            if command == "pedestrian_access":
                led = LED(2, active_high=False)
                led.on()
                sleep(0.2)
                led.off()
                led.close()
                self.send(text_data=json.dumps({'result': 'gate_triggered'}))
                MailSender.sendMail("Pedestrian access triggered")
                return
            elif command == "vehicle_access":
                led = LED(3, active_high=False)
                led.on()
                sleep(0.2)
                led.off()
                led.close()
                self.send(text_data=json.dumps({'result': 'gate_triggered'}))
                MailSender.sendMail("Vehicle access triggered")
                return
            self.send(text_data=json.dumps({'result': 'bad_command'}))
            MailSender.sendMail("Gate trigger failed with bad command")
        except Exception as e:            
            self.send(text_data=json.dumps({'result': 'internal_server_error'}))
            MailSender.sendMail(f"Gate trigger failed with exception: {e}")
