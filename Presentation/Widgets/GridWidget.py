from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation

class GridWidget(Widget):
    def __init__(self, gridWidth, gridHeight, lineWidth = 1):
        super().__init__()
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.lineWidth = lineWidth
        self.gridWidgets = {}
        self.canAnimate = True

    def on_size_update(self):
        self.drawGrid()
        self.updateWidgetsPositions()

    def gridPositionAt(self, position): 
        if not self.collide_point(*position):
            return None
        (columnWidth, lineHeight) = self.gridItemSize()
        positionX = int((position[0] - self.pos[0])/columnWidth)
        positionY = int((position[1] - self.pos[1])/lineHeight)

        return (positionX, positionY)

    def gridItemSize(self):
        return (self.width/self.gridWidth, self.height/self.gridHeight)

    def positionForGridPosition(self, gridPosition): 
        (columnWidth, lineHeight) = self.gridItemSize()
        return (self.pos[0] + columnWidth * gridPosition[0], self.pos[1] + lineHeight * gridPosition[1])

    def moveWidgetInSequence(self, widget, sequence, didFinishSequenceAnimation):
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition == None: 
            return

        if not self.canAnimate:
            return

        if len(sequence) == 0:
            didFinishSequenceAnimation(widget)
            return

        animations = [Animation(x = position[0], y = position[1], duration = 0.2) for position in [self.positionForGridPosition(gridPosition) for gridPosition in sequence]]
        aninationsSequence = AnimationListSequence(animations)
        aninationsSequence.sequence.bind(on_complete=lambda _, __: self.finishAnimation(widget, sequence[-1], didFinishSequenceAnimation))
        
        aninationsSequence.sequence.start(widget)
        self.canAnimate = False

    def finishAnimation(self, widget, targetPosition, didFinishSequenceAnimation):
        self.canAnimate = True
        self.moveWidgetToGridPosition(widget, targetPosition)
        didFinishSequenceAnimation(widget)

    def addWidgetToGridPosition(self, widget, gridPosition):
        self.setPositionForWidgetAtGridPosition(widget, gridPosition)

        if gridPosition in self.gridWidgets:
            self.gridWidgets[gridPosition].append(widget)
        else:
            self.gridWidgets[gridPosition] = [widget]

        self.add_widget(widget)

    def removeWidget(self, widget):
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition == None: 
            return

        del self.gridWidgets[widgetPosition[0]][widgetPosition[1]]
        self.remove_widget(widget)

    def moveWidgetFromPositionToGridPosition(self, oldGridPosition, newGridPosition):
        if self.gridWidgets[oldGridPosition[0]] == None or len(self.gridWidgets[oldGridPosition[0]]) == 0: 
            return False
        widget = self.gridWidgets[oldGridPosition[0]][oldGridPosition[1]]
        self.setPositionForWidgetAtGridPosition(widget, newGridPosition)
        self.gridWidgets[oldGridPosition[0]].remove(widget)

        if newGridPosition in self.gridWidgets:
            self.gridWidgets[newGridPosition].append(widget)
        else:
            self.gridWidgets[newGridPosition] = [widget]

        return True

    def moveWidgetToGridPosition(self, widget, gridPosition):
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition is None:
            return False

        widgetOldPosition = widgetPosition[0]
        return self.moveWidgetFromPositionToGridPosition(widgetPosition, gridPosition)

    def widgetGridPosition(self, widget):
        return self.getWidgetPosition(widget)[0]

    def getWidgetPosition(self, widget):
        widgetOldPositions = [
            (gridPosition, widgets) for (gridPosition, widgets) in self.gridWidgets.items() if widget in widgets
        ]

        if not any(widgetOldPositions): 
            return None

        widgetGridPosition = widgetOldPositions[0][0]

        try: 
            return (widgetGridPosition, widgetOldPositions[0][1].index(widget))
        except:
            return None

    def setPositionForWidgetAtGridPosition(self, widget, gridPosition): 
        (positionX, positionY) = self.positionForGridPosition(gridPosition)

        widget.pos = (positionX, positionY)
        widget.size = self.gridItemSize()

    def moveWidgetFromPositionByDirection(self, gridPosition, direction): 
        newGridPosition = (gridPosition[0][0] + direction.value[0], gridPosition[0][1] + direction.value[1])
        return self.moveWidgetFromPositionToGridPosition(gridPosition, newGridPosition)

    def moveWidgetByDirection(self, widget, direction): 
        widgetPosition = self.getWidgetPosition(widget)

        if widgetPosition is None:
            return False

        return self.moveWidgetFromPositionByDirection(widgetPosition, direction)

    def updateWidgetsPositions(self):
        for (gridPosition, widgets) in self.gridWidgets.items():
            for widget in widgets:
                self.setPositionForWidgetAtGridPosition(widget, gridPosition)

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

class AnimationListSequence(Animation):
    def __init__(self, sequence):   
        super().__init__()
        firstAnimation = sequence.pop(0)
        self.sequence = AnimationListSequence.listSequence(sequence, firstAnimation)
        
    def listSequence(sequence, currentAnimation):
        if len(sequence) == 0:
            return currentAnimation
        animation = sequence.pop(0)
        return AnimationListSequence.listSequence(sequence, currentAnimation + animation)