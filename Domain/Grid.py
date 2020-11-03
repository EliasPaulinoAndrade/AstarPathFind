from enum import Enum
from .Direction import Direction

class GridItemType(Enum): 
    EMPTY = 0
    WALL = 1

class GridItem:
    def __init__(self, position, itemType):
        self.itemType = itemType
        self.position = position

class CostGridItem:
    def __init__(self, estimatedDistanceToEnd, distanceToBegin, position, parentItem):
        self.estimatedDistanceToEnd = estimatedDistanceToEnd
        self.distanceToBegin = distanceToBegin
        self.cost = estimatedDistanceToEnd + distanceToBegin
        self.position = position
        self.parentItem = parentItem

class GridPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "{x: " + str(self.x) + ", y: " + str(self.y) + "}" 
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Grid: 
    def __init__(self, gridWidth, gridHeight, initialState):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.grid = initialState

    def __iter__(self):
        return (
            GridItem(GridPosition(columnIndex, rowIndex), GridItemType(self.grid[rowIndex][columnIndex])) 
                for columnIndex in range(self.gridWidth) 
                    for rowIndex in range(self.gridHeight)
        ) 

    def __getitem__(self, position):
        if position.x < self.gridWidth and position.x >= 0 and position.y < self.gridHeight and position.y >= 0:
             return GridItem(GridPosition(position.x, position.y), GridItemType(self.grid[position.y][position.x]))
        return None

    def emptyGridItems(self):
        return [gridItem for gridItem in self if gridItem.itemType == GridItemType.EMPTY]

    def findPath(self, startPosition, endPosition): 
        if self[startPosition].itemType == GridItemType.WALL.value or self[endPosition].itemType == GridItemType.WALL.value: 
            return None

        closedList = []
        startItem = Grid.costItemAtPosition(startPosition, startPosition, endPosition, None)
        currentItem = None
        openList = [startItem]

        while len(openList) != 0:
            #order by coast
            openList = sorted(openList, reverse = True, key = lambda gridItem: gridItem.cost)

            #get the lowest coast item
            currentItem = openList.pop()
            closedList.append(currentItem)

            if currentItem.position == endPosition:
                return Grid.getPathToItem(currentItem)
            
            openList += self.adjacentItems(currentItem.position, startPosition, endPosition, currentItem, closedList, openList)

    def getPathToItem(gridItem, currentPath = []):
        if gridItem.parentItem is None:
            return currentPath
        return Grid.getPathToItem(gridItem.parentItem, [gridItem.position] + currentPath)

    def adjacentItems(self, position, startPosition, endPosition, currentItem, closedList, openList):
        return [ 
            gridItem for gridItem in
            [
                Grid.costItemAtPosition(
                    Grid.positionAtDirection(position, direction), 
                    startPosition, 
                    endPosition,
                    currentItem
                ) for direction in Direction
            ]
            if self.positionIsWalkable(gridItem.position) and Grid.itemIsValid(gridItem, closedList, openList)
        ]

    def itemIsValid(gridItem, closedList, openList):
        if any([closedItem.position == gridItem.position for closedItem in closedList]):
            return False
        if any([openedItem.position == gridItem.position for openedItem in closedList]):
            return False
        return True

    def positionIsWalkable(self, position):
        itemAtPosition = self[position] 
        return itemAtPosition != None and itemAtPosition.itemType != GridItemType.WALL

    def costItemAtPosition(position, startPosition, endPosition, parentNode):
        if parentNode is None:
            return CostGridItem(0, Grid.estimatedDistance(position, endPosition), position, parentNode)
        return CostGridItem(parentNode.distanceToBegin + 1, Grid.estimatedDistance(position, endPosition), position, parentNode)

    def estimatedDistance(fromPosition, toPosition):
        return pow(fromPosition.x - toPosition.x, 2) + pow(fromPosition.y - toPosition.y, 2)

    def positionAtDirection(position, direction):
        return GridPosition(position.x + direction.value[0], position.y + direction.value[1])