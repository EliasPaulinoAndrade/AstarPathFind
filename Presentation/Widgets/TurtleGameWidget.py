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
    followWormSwitch = ObjectProperty(None) 

    def __init__(self):
        super().__init__()
        print(self.followWormSwitch)

class TurtleGameWidget(Widget):
    turtleWidget = Image(source=Images.turtle.value)
    wormWidget = Image(source=Images.worm.value)

    def __init__(self, grid, gridWidth, gridHeight, wormPosition, turtlePosition):
        super().__init__()
        self.grid = grid
        self.menuWidget = MenuWidget()
        self.gridWidget = GridWidget(gridWidth, gridHeight, 0)
        self.wormPosition = wormPosition
        self.gridWidget.addWidgetToGridPosition(self.wormWidget, wormPosition)
        self.gridWidget.addWidgetToGridPosition(self.turtleWidget, turtlePosition)

        self.bind(size=self.on_size_update)
        self.menuWidget.followWormSwitch.bind(active=self.followWormHasSwitched)
        self.add_widget(self.menuWidget)
        self.add_widget(self.gridWidget)
        self.addWalls()

    def followWormHasSwitched(self, _, __):
        if self.menuWidget.followWormSwitch.active:
            self.moveTurtleToGridPosition(GridPosition(self.wormPosition[0], self.wormPosition[1]))
        
    def on_size_update(self, width, height):
        gridSize = min(self.size[0], self.size[1])
        menuHeight = 100
        turtleGridHeight = gridSize - menuHeight

        self.gridWidget.width = gridSize
        self.gridWidget.height = gridSize - menuHeight
        self.gridWidget.center_x = self.center_x
        self.gridWidget.top = self.top

        self.menuWidget.width = gridSize
        self.menuWidget.height = menuHeight
        self.menuWidget.center_x = self.center_x

        self.gridWidget.on_size_update()

    def addWalls(self):
        [self.gridWidget.addWidgetToGridPosition(Image(source=Images.wall.value, allow_stretch = True, keep_ratio = False), (wallGridItem.position.x, wallGridItem.position.y)) 
            for wallGridItem in [gridItem 
                for gridItem in self.grid if gridItem.itemType == GridItemType.WALL
            ]
        ]

    def on_touch_down(self, touch):
        self.menuWidget.on_touch_down(touch)
        touchedPosition = self.gridWidget.gridPositionAt(touch.pos)

        if touchedPosition == None: 
            return 
        
        self.gridWidget.addWidgetToGridPosition(TouchFeedbackWidget(self.finishedAnimation), touchedPosition)

        toGridPosition = GridPosition(touchedPosition[0], touchedPosition[1])   
        self.moveTurtleToGridPosition(toGridPosition)
    
    def moveTurtleToGridPosition(self, toGridPosition):
        turtlePosition = self.gridWidget.widgetGridPosition(self.turtleWidget)
        fromGridPosition = GridPosition(turtlePosition[0], turtlePosition[1])
        turtlePath = self.grid.findPath(fromGridPosition, toGridPosition)

        if turtlePath is None:
            return
        
        pathPositions = [(position.x, position.y) for position in turtlePath]
        self.gridWidget.moveWidgetInSequence(self.turtleWidget, pathPositions, self.didFinishSequenceAnimation)

    def didFinishSequenceAnimation(self, widget):
        turtleGridPosition = self.gridWidget.widgetGridPosition(self.turtleWidget)
        wormGridPosition = self.gridWidget.widgetGridPosition(self.wormWidget)

        if turtleGridPosition is None or wormGridPosition is None:
            return 
        
        if wormGridPosition == turtleGridPosition:
            self.moveWormToRandomPosition()

    def moveWormToRandomPosition(self):
        emptyGridItems = self.grid.emptyGridItems()
        randomEmptyItem = choice(emptyGridItems)

        newWormPosition = (randomEmptyItem.position.x, randomEmptyItem.position.y)
        self.wormPosition = newWormPosition

        self.gridWidget.moveWidgetToGridPosition(self.wormWidget, newWormPosition)

        if self.menuWidget.followWormSwitch.active:
            self.moveTurtleToGridPosition(randomEmptyItem.position)

    def finishedAnimation(self, touchWidget):
        self.gridWidget.removeWidget(touchWidget)