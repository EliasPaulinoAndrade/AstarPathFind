from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch

class MenuWidget(Widget):   
    followWormSwitch = ObjectProperty(None) 

    def __init__(self):
        super().__init__()
        print(self.followWormSwitch)