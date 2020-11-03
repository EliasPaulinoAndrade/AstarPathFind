
class CostGridItem:
    def __init__(self, estimatedDistanceToEnd, distanceToBegin, position, parentItem):
        self.estimatedDistanceToEnd = estimatedDistanceToEnd
        self.distanceToBegin = distanceToBegin
        self.cost = estimatedDistanceToEnd + distanceToBegin
        self.position = position
        self.parentItem = parentItem
