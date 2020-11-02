from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics import Color, Rectangle
from Direction import Direction

class Grid(Widget):
    def __init__(self, gridWidth, gridHeight, lineWidth = 1):
        super().__init__()
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.lineWidth = lineWidth
        self.gridWidgets = {}

    def on_size_update(self):
        gridSize = min(self.parent.size[0], self.parent.size[1])
        self.width = self.height = gridSize
        self.center = self.parent.center
        self.drawGrid()
        self.updateWidgetsPositions()

    def gridItemSize(self):
        return (self.width/self.gridWidth, self.height/self.gridHeight)

    def positionForGridPosition(self, gridPosition): 
        (columnWidth, lineHeight) = self.gridItemSize()
        return (self.pos[0] + columnWidth * gridPosition[0], self.pos[1] + lineHeight * gridPosition[1])

    def addWidgetToGridPosition(self, widget, gridPosition):
        self.setPositionForWidgetAtGridPosition(widget, gridPosition)
        self.gridWidgets[gridPosition] = widget
        self.add_widget(widget)
        

    def moveWidgetFromPositionToGridPosition(self, oldGridPosition, newGridPosition):
        if newGridPosition in self.gridWidgets: 
            return False
        
        widget = self.gridWidgets[oldGridPosition]
        self.setPositionForWidgetAtGridPosition(widget, newGridPosition)
        del self.gridWidgets[oldGridPosition]
        self.gridWidgets[newGridPosition] = widget

        return True

    def moveWidgetToGridPosition(self, widget, gridPosition):
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition is None:
            return False

        widgetOldPosition = widgetPosition[0]
        return self.moveWidgetFromPositionToGridPosition(widgetPosition, gridPosition)

    def getWidgetPosition(self, widget):
        widgetOldPositions = [
            gridPosition for (gridPosition, widgetAtPosition) in self.gridWidgets.items() if widget == widgetAtPosition
        ]
        
        if len(widgetOldPositions) == 0: 
            return nil

        return widgetOldPositions[0]

    def setPositionForWidgetAtGridPosition(self, widget, gridPosition): 
        (positionX, positionY) = self.positionForGridPosition(gridPosition)

        widget.pos = (positionX, positionY)
        widget.size = self.gridItemSize()

    def moveWidgetFromPositionByDirection(self, gridPosition, direction): 
        newGridPosition = (gridPosition[0] + direction.value[0], gridPosition[1] + direction.value[1])
        return self.moveWidgetFromPositionToGridPosition(gridPosition, newGridPosition)

    def moveWidgetByDirection(self, widget, direction): 
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition is None:
            return False

        return self.moveWidgetFromPositionByDirection(widgetPosition, direction)

    def updateWidgetsPositions(self):
        {self.setPositionForWidgetAtGridPosition(widget, gridPosition) for (gridPosition, widget) in self.gridWidgets.items()}

    def drawGrid(self):
        (columnWidth, lineHeight) = self.gridItemSize()
        self.canvas.before.clear()

        with self.canvas.before:  
            Color(1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0, 0, 0, 0.2)
            [Line(
                points = [
                    self.pos[0] + columnWidth * column, self.pos[1], 
                    self.pos[0] + columnWidth * column, self.pos[1] + self.height
                ], 
                width = self.lineWidth
                ) for column in range(self.gridWidth + 1)
            ]
            [Line(
                points = [
                    self.pos[0], self.pos[1] + lineHeight * row,
                    self.pos[0] + self.width, self.pos[1] + lineHeight * row,
                ], 
                width = self.lineWidth
                ) for row in range(self.gridHeight + 1)
            ]
