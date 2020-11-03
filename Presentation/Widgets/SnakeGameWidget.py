from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from ..Resources.Images import Images
from .GridWidget import GridWidget
from .TouchFeedbackWidget import TouchFeedbackWidget
from Domain.Grid import Grid, GridItem, GridItemType, GridPosition
from kivy.properties import ObjectProperty

from random import choice

class MenuWidget(Widget):   
    followRatSwitch = ObjectProperty(None)

    def __init__(self):
        super().__init__()    
        print(self.followRatSwitch)   

class SnakeGameWidget(Widget):
    snakeWidget = Image(source=Images.snake.value)
    ratWidget = Image(source=Images.rat.value)

    def __init__(self, grid, gridWidth, gridHeight, ratPosition, snakePosition):
        super().__init__()
        self.grid = grid
        self.menuWidget = MenuWidget()
        self.snakeGrid = GridWidget(gridWidth, gridHeight, 0)
        self.ratPosition = ratPosition
        self.snakeGrid.addWidgetToGridPosition(self.ratWidget, ratPosition)
        self.snakeGrid.addWidgetToGridPosition(self.snakeWidget, snakePosition)

        self.bind(size=self.on_size_update)
        self.menuWidget.followRatSwitch.bind(active=self.followRatHasSwitched)
        self.add_widget(self.menuWidget)
        self.add_widget(self.snakeGrid)
        self.addWalls()

    def followRatHasSwitched(self, _, __):
        if self.menuWidget.followRatSwitch.active:
            self.moveSnakeToGridPosition(GridPosition(self.ratPosition[0], self.ratPosition[1]))
        
    def on_size_update(self, width, height):
        gridSize = min(self.size[0], self.size[1])
        menuHeight = 100
        snakeGridHeight = gridSize - menuHeight

        self.snakeGrid.width = gridSize
        self.snakeGrid.height = gridSize - menuHeight
        self.snakeGrid.center_x = self.center_x
        self.snakeGrid.top = self.top

        self.menuWidget.width = gridSize
        self.menuWidget.height = menuHeight
        self.menuWidget.center_x = self.center_x

        self.snakeGrid.on_size_update()

    def addWalls(self):
        [self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value, allow_stretch = True, keep_ratio = False), (wallGridItem.position.x, wallGridItem.position.y)) 
            for wallGridItem in [gridItem 
                for gridItem in self.grid if gridItem.itemType == GridItemType.WALL
            ]
        ]

    def on_touch_down(self, touch):
        self.menuWidget.on_touch_down(touch)
        touchedPosition = self.snakeGrid.gridPositionAt(touch.pos)

        if touchedPosition == None: 
            return 
        
        self.snakeGrid.addWidgetToGridPosition(TouchFeedbackWidget(self.finishedAnimation), touchedPosition)

        toGridPosition = GridPosition(touchedPosition[0], touchedPosition[1])   
        self.moveSnakeToGridPosition(toGridPosition)
    
    def moveSnakeToGridPosition(self, toGridPosition):
        snakePosition = self.snakeGrid.widgetGridPosition(self.snakeWidget)
        fromGridPosition = GridPosition(snakePosition[0], snakePosition[1])
        snakePath = self.grid.findPath(fromGridPosition, toGridPosition)

        if snakePath is None:
            return
        
        pathPositions = [(position.x, position.y) for position in snakePath]
        self.snakeGrid.moveWidgetInSequence(self.snakeWidget, pathPositions, self.didFinishSequenceAnimation)

    def didFinishSequenceAnimation(self, widget):
        snakeGridPosition = self.snakeGrid.widgetGridPosition(self.snakeWidget)
        ratGridPosition = self.snakeGrid.widgetGridPosition(self.ratWidget)

        if snakeGridPosition is None or ratGridPosition is None:
            return 
        
        if ratGridPosition == snakeGridPosition:
            self.moveRatToRandomPosition()

    def moveRatToRandomPosition(self):
        emptyGridItems = self.grid.emptyGridItems()
        randomEmptyItem = choice(emptyGridItems)

        newRatPosition = (randomEmptyItem.position.x, randomEmptyItem.position.y)
        self.ratPosition = newRatPosition

        self.snakeGrid.moveWidgetToGridPosition(self.ratWidget, newRatPosition)

        if self.menuWidget.followRatSwitch.active:
            self.moveSnakeToGridPosition(randomEmptyItem.position)

    def finishedAnimation(self, touchWidget):
        self.snakeGrid.removeWidget(touchWidget)