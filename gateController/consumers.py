import json
from channels.generic.websocket import WebsocketConsumer

class GateTriggerConsumer(WebsocketConsumer):
    def connect(self):
        import time
        time.sleep(2)
        self.accept()
        print("Connected")

    def disconnect(self, close_code):
        print("Disconnected")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']

        self.send(text_data=json.dumps({
            'result': 'gate_triggered'
        }))