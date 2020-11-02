from kivy.uix.widget import Widget
from kivy.uix.image import Image
from Images import Images
from Grid import Grid

class SnakeGame(Widget):
    snakeGrid = Grid(20, 20, 0)
    snakeWidget = Image(source=Images.snake.value)
    ratWidget = Image(source=Images.rat.value)

    def __init__(self):
        super().__init__()
        self.bind(size=self.on_size_update)
        self.add_widget(self.snakeGrid)
        self.snakeGrid.addWidgetToGridPosition(self.snakeWidget, (2, 2))

        self.snakeGrid.addWidgetToGridPosition(self.ratWidget, (10, 10))
        self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 3))
        self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 4))
        self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 5))
        self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (4, 3))
        self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (5, 3))
        
    def on_size_update(self, width, height):
        self.snakeGrid.on_size_update()
