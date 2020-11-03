from kivy.uix.widget import Widget
from kivy.uix.image import Image
from ..Resources.Images import Images
from .GridWidget import GridWidget
from .TouchFeedbackWidget import TouchFeedbackWidget
from Domain.Grid import Grid, GridItem, GridItemType, GridPosition

class SnakeGameWidget(Widget):
    snakeWidget = Image(source=Images.snake.value)
    ratWidget = Image(source=Images.rat.value)

    def __init__(self, grid, gridWidth, gridHeight):
        super().__init__()
        self.grid = grid
        self.snakeGrid = GridWidget(gridWidth, gridHeight, 0)
        self.bind(size=self.on_size_update)
        self.add_widget(self.snakeGrid)
        
        self.snakeGrid.addWidgetToGridPosition(self.snakeWidget, (2, 2))
        self.snakeGrid.addWidgetToGridPosition(self.ratWidget, (5, 0))
        self.addWalls()
        
    def on_size_update(self, width, height):
        self.snakeGrid.on_size_update()

    def addWalls(self):
        [self.snakeGrid.addWidgetToGridPosition(Image(source=Images.wall.value, allow_stretch = True, keep_ratio = False), (wallGridItem.position.x, wallGridItem.position.y)) 
            for wallGridItem in [gridItem 
                for gridItem in self.grid if gridItem.itemType == GridItemType.WALL
            ]
        ]

    def on_touch_down(self, touch):
        touchedPosition = self.snakeGrid.gridPositionAt(touch.pos)
        snakePosition = self.snakeGrid.widgetGridPosition(self.snakeWidget)

        if touchedPosition == None: 
            return 
        
        self.snakeGrid.addWidgetToGridPosition(TouchFeedbackWidget(self.finishedAnimation), touchedPosition)

        fromGridPosition = GridPosition(snakePosition[0], snakePosition[1])
        toGridPosition = GridPosition(touchedPosition[0], touchedPosition[1])   
        snakePath = self.grid.findPath(fromGridPosition, toGridPosition)

        if snakePath is None:
            return
        
        pathPositions = [(position.x, position.y) for position in snakePath]
        self.snakeGrid.moveWidgetInSequence(self.snakeWidget, pathPositions)

    def finishedAnimation(self, touchWidget):
        self.snakeGrid.removeWidget(touchWidget)