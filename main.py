import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.config import Config

#import socket
import paho.mqtt.client as mqtt
import time



class Grid(Widget):
    button_id = ObjectProperty(None)

    def press(self):
        exit()


    
class  ControlPanel(App):

    popup = Popup(title='Connection error',content=Label(text='The application can not reach the server.\n Please check if you are connected  to the proper network \n and restart the application.'),
    size_hint=(None, None), size=(300, 300), auto_dismiss=False)
    
    client = mqtt.Client()
    broker = "192.168.1.110"
    port = 1885
    sub_topics = [("data/room_Jann",0)  ,  ("data/external_sensors",0)]



    def on_connect(self,client, userdata, flags, rc):
        print("--------------------  Connected with result code "+str(rc))
        self.client.subscribe(self.sub_topics)


    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        

    def on_start(self, **kwargs):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(self.broker,self.port,60)
            self.client.loop_start()
        except Exception as e:
            print("timeout", e)
            self.popup.open()


    def build(self):
        return Grid()
    
    def on_pause(self):
        self.client.disconnect()

    def on_resume(self):
        on_start()



#sending functions
    def btn_lamp_on(self):
        self.client.publish("control/socket", payload="1")

    def btn_lamp_off(self):
        self.client.publish("control/socket", payload="0")

    def btn_blind_close(self):
        self.client.publish("control/room_Jan/device_blinds", payload="0")

    def btn_blind_open(self):
        self.client.publish("control/room_Jan/device_blinds", payload="1") 

    def btn_desktopLamp_on(self):
        self.client.publish("control/room_Jan/device_lamp", payload="1") 

    def btn_desktopLamp_off(self):
        self.client.publish("control/room_Jan/device_lamp", payload="0") 


if __name__=="__main__":
    Config.set('graphics', 'width', '500')
    Config.set('graphics', 'height', '800')
    ControlPanel().run()
