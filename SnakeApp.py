from kivy.app import App
from TurtleGame import TurtleGame
from kivy.clock import Clock

class TurtleApp(App):

    def build(self):
        turtleGame = TurtleGame()
        return turtleGame

if __name__ == '__main__':
    TurtleApp().run()