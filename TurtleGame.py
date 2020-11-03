from kivy.uix.widget import Widget
from kivy.uix.image import Image
from Images import Images
from Grid import Grid

class TurtleGame(Widget):
    turtleGrid = Grid(20, 20, 0)
    turtleWidget = Image(source=Images.turtle.value)
    wormWidget = Image(source=Images.worm.value)

    def __init__(self):
        super().__init__()
        self.bind(size=self.on_size_update)
        self.add_widget(self.turtleGrid)
        self.turtleGrid.addWidgetToGridPosition(self.turtleWidget, (2, 2))

        self.turtleGrid.addWidgetToGridPosition(self.wormWidget, (10, 10))
        self.turtleGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 3))
        self.turtleGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 4))
        self.turtleGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (3, 5))
        self.turtleGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (4, 3))
        self.turtleGrid.addWidgetToGridPosition(Image(source=Images.wall.value), (5, 3))
        
    def on_size_update(self, width, height):
        self.turtleGrid.on_size_update()
