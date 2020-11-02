from kivy.app import App
from SnakeGame import SnakeGame
from kivy.clock import Clock

class SnakeApp(App):

    def build(self):
        snakeGame = SnakeGame()
        return snakeGame

if __name__ == '__main__':
    SnakeApp().run()