from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.animation import Animation

class TouchFeedbackWidget(Widget):
    bg_color = ObjectProperty([1, 1, 1, 1])

    def __init__(self, finishedAnimation):
        super().__init__()
        self.startPulsing()
        self.finishedAnimation = finishedAnimation
        self.bg_color = [1,1,1,0]

    def startPulsing(self, *args):
        anim = Animation(bg_color=[0,1,0,0.2]) + Animation(bg_color=[1,1,1,0])
        anim.repeat = False
        anim.start(self)
        anim.bind(on_complete = self.hasFinishedAnimation)

    def hasFinishedAnimation(self, _, __):
        self.finishedAnimation(self)